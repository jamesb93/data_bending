# -*- coding: utf-8 -*-
import docker
import inspect
import pytest
import os
import re
import argparse
import shutil
import subprocess as sp
import webbrowser


NAME = "forensicarchitecture/mtriage"
CONT_NAME = NAME.replace("/", "_")  # docker doesn't allow slashes in cont names

SERVER_NAME = "forensicarchitecture/mtriageserver"
CONT_SERVER_NAME = SERVER_NAME.replace("/", "_")

VIEWER_NAME = "forensicarchitecture/mtriageviewer"
CONT_VIEWER_NAME = VIEWER_NAME.replace("/", "_")

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ENV_FILE = "{}/.env".format(DIR_PATH)
HOME_PATH = os.path.expanduser("~")
DOCKER = docker.from_env()


def get_subdirs(d):
    whitelist = ["__pycache__"]
    return [
        o
        for o in os.listdir(d)
        if os.path.isdir(os.path.join(d, o)) and o not in whitelist
    ]


class InvalidPipDep(Exception):
    pass


class InvalidArgumentsError(Exception):
    pass


def name_and_ver(pipdep):
    """ Return the name and version from a string that expresses a pip dependency.
        Raises an InvalidPipDep exception if the string is an invalid dependency.
    """
    pipdep = pipdep.split("==")
    dep_name = pipdep[0]
    try:
        if len(pipdep) == 1:
            dep_version = None
        elif len(pipdep) > 2:
            raise InvalidPipDep
        else:
            dep_version = pipdep[1]
            if re.search(r"^([0-9]{1,2}\.){0,2}([0-9]{1,2})$", dep_version) is None:
                raise InvalidPipDep
        return dep_name, dep_version
    except:
        raise InvalidPipDep


def should_add_pipdep(dep, pipdeps):
    """Check whether pipdep should be added.
    """
    dep_name, dep_ver = name_and_ver(dep)
    for _dep in pipdeps:
        _dep_name, _dep_ver = name_and_ver(_dep)
        if _dep_name == dep_name:
            # new version unspecified, cannot be more specific
            if dep_ver is None:
                return False
            # new version more specific
            elif _dep_ver is None and dep_ver is not None:
                return True
            elif str(dep_ver) < str(_dep_ver):
                return False
    return True


def should_add_dockerline(line, dockerfile):
    """Check whether line should be added to array representing Dockerfile.
    """
    return line not in dockerfile


def add_deps(dep_path, deps, should_add):
    """ Add dependences at {folder_path} to {deps}, excluding if {should_add} is True for any given dependency.
    """
    if not os.path.isfile(dep_path):
        return

    with open(dep_path) as f:
        for line in f.readlines():
            if should_add(line, deps):
                deps.append(line)


def build(args):
    """ Collect all partial Pip and Docker files from selectors and analysers, and combine them with the core mtriage
        dependencies in src/build in order to create an appropriate Dockerfile and requirements.txt.
        NOTE: There is currently no way to include/exclude certain selector dependencies, but this build process is
              the setup for that optionality.
    """

    IS_GPU = args.gpu

    # setup
    TAG_NAME = "dev-gpu" if IS_GPU else "dev"
    DOCKER_BASE = "core-gpu" if IS_GPU else "core-cpu"

    DOCKERFILE_PARTIAL = "partial.Dockerfile"
    PIP_PARTIAL = "requirements.txt"
    BUILD_DOCKERFILE = "{}/build.Dockerfile".format(DIR_PATH)
    BUILD_PIPFILE = "{}/build.requirements.txt".format(DIR_PATH)
    CORE_PIPDEPS = "{}/src/build/core.requirements.txt".format(DIR_PATH)
    CORE_START_DOCKER = "{}/src/build/{}.start.Dockerfile".format(DIR_PATH, DOCKER_BASE)
    CORE_END_DOCKER = "{}/src/build/core.end.Dockerfile".format(DIR_PATH)
    ANALYSERS_PATH = "{}/src/lib/analysers".format(DIR_PATH)
    SELECTORS_PATH = "{}/src/lib/selectors".format(DIR_PATH)

    print("Collecting partial dependencies from selector and analyser folders...")

    with open(CORE_PIPDEPS) as cdeps:
        pipdeps = cdeps.readlines()

    with open(CORE_START_DOCKER) as dfile:
        dockerlines = dfile.readlines()

    # search all selectors/analysers for partials
    selectors = get_subdirs(SELECTORS_PATH)
    analysers = get_subdirs(ANALYSERS_PATH)

    for selector in selectors:
        docker_dep = "{}/{}/{}".format(SELECTORS_PATH, selector, DOCKERFILE_PARTIAL)
        pip_dep = "{}/{}/{}".format(SELECTORS_PATH, selector, PIP_PARTIAL)

        add_deps(docker_dep, dockerlines, should_add_dockerline)
        add_deps(pip_dep, pipdeps, should_add_pipdep)

    for analyser in analysers:
        docker_dep = "{}/{}/{}".format(ANALYSERS_PATH, analyser, DOCKERFILE_PARTIAL)
        pip_dep = "{}/{}/{}".format(ANALYSERS_PATH, analyser, PIP_PARTIAL)

        add_deps(docker_dep, dockerlines, should_add_dockerline)
        add_deps(pip_dep, pipdeps, should_add_pipdep)

    with open(CORE_END_DOCKER) as f:
        for line in f.readlines():
            dockerlines.append(line)

    # create Dockerfile and requirements.txt for build
    # if os.path.exists(BUILD_PIPFILE):
    #     os.remove(BUILD_PIPFILE)

    with open(BUILD_PIPFILE, "w") as f:
        for dep in pipdeps:
            f.write(dep)

    # if os.path.exists(BUILD_DOCKERFILE):
    #     os.remove(BUILD_DOCKERFILE)

    with open(BUILD_DOCKERFILE, "w") as f:
        for line in dockerlines:
            f.write(line)

    print("All Docker dependencies collected in build.Dockerfile.")
    print("All Pip dependencies collected in build.requirements.txt.")
    print("--------------------------------------------------------")
    if IS_GPU:
        print("GPU flag enabled, building for nvidia-docker...")
    else:
        print("Building for CPU in Docker...")

    try:
        sp.call(
            [
                "docker",
                "build",
                "-t",
                "{}:{}".format(NAME, TAG_NAME),
                "-f",
                BUILD_DOCKERFILE,
                ".",
            ]
        )
        print("Build successful, run with: \n\tpython run.py develop")
    except:
        print("Something went wrong! EEK.")

    # cleanup
    os.remove(BUILD_DOCKERFILE)
    os.remove(BUILD_PIPFILE)


def develop(args):
    TAG_NAME = "dev-gpu" if args.gpu else "dev"
    # --runtime only exists on nvidia docker, so we pass a bubblegum flag when not available
    # so that the call arguments are well formed.
    try:
        DOCKER.containers.get(CONT_NAME)
        print("Develop container already running. Stop it and try again.")
    except docker.errors.NotFound:
        sp.call(
            [
                "docker",
                "run",
                "-it",
                "--name",
                CONT_NAME,
                "--runtime=nvidia" if args.gpu else "--ipc=host",
                "--env",
                "BASE_DIR=/mtriage",
                "--env-file={}".format(ENV_FILE),
                "--rm",
                "--privileged",
                "-v",
                "{}:/mtriage".format(DIR_PATH),
                "-v",
                "{}/.config/gcloud:/root/.config/gcloud".format(HOME_PATH),
                "{}:{}".format(NAME, TAG_NAME),
            ]
        )


def clean(args):
    sp.call(["docker", "rmi", NAME])


def __run_lib_tests():
    returncode = sp.call(
        [
            "docker",
            "run",
            "--env",
            "BASE_DIR=/mtriage",
            "--env-file={}".format(ENV_FILE),
            "--rm",
            "-v",
            "{}:/mtriage".format(DIR_PATH),
            "--workdir",
            "/mtriage/src",
            "{}:dev".format(NAME),
            "python",
            "-m",
            "pytest",
            "test",
        ]
    )
    if returncode is 1:
        exit(returncode)


def __run_runpy_tests():
    # NOTE: runpy tests are not run in a docker container, as they operate on the local machine-- so this test is run
    # using the LOCAL python (could be 2 or 3).
    returncode = sp.call(["python", "-m", "pytest", "test/"])
    if returncode is 1:
        exit(returncode)


def test(args):
    print("Creating container to run tests...")
    print("----------------------------------")
    __run_lib_tests()
    __run_runpy_tests()
    print("----------------------------------")
    print("All tests for mtriage done.")


def viewer(args):

    """ Must be invoked with an input folder and viewer-plugin e.g.:

            python run.py viewer -i <derived_folder> -v <viewer_plugin>

        Server requires that input folder contains directories corresponsing to elements (where directory names
        are element ids.) Each element directory must contain a json file containing:

        {
            "id": <element_id>,
            "media": [
                <media1.mp3>
                <media1.mp4>,
                <media1.png>,
                etc.
            ]
        }

        As well as any other data to be consumed by the viewr-plugin. Media are any other files
        in the element folder that need to be available to the viewer-plugin.

        Viewers must be yarn buildable apps living in the src/lib/viewers folder. Their name is taken to be the name
        of their outer directory.

        Once launched the viewer plugin is available at http://localhost:8081/

        The server is available at http://localhost:8080/, with available endpoints:

        elements                                    - returns list of element ids
        element?id=<element_id>                     - serves the element's json file
        element?if=<element_id>&media=<media_file>  - serves the media file associated with element

    """

    folder = args.input
    viewer = args.viewer

    if args.input == None:
        raise InvalidArgumentsError("No input directory supplied for viewer plugin.")

    if args.viewer == None:
        raise InvalidArgumentsError("No viewer plugin name supplied.")

    if not os.path.exists(folder):
        raise WorkingDirectorNotFoundError(folder)

    shutil.rmtree("src/server/elements/")
    os.makedirs("src/server/elements/")

    element_folders = [f for f in os.listdir(folder) if os.path.isdir(folder + "/" + f)]

    for e in element_folders:
        f = str(folder) + "/" + str(e)
        for file in os.listdir(f):
            if not os.path.exists("src/server/elements/" + e):
                os.makedirs("src/server/elements/" + e)
            os.symlink(
                "/mtriage/" + f + "/" + file, "src/server/elements/" + e + "/" + file
            )

    print("Creating container to build server...")
    print("----------------------------------")
    try:
        sp.call(
            [
                "docker",
                "build",
                "-t",
                "{}:dev".format(SERVER_NAME),
                "-f",
                "src/server/server.Dockerfile",
                "src/server",
            ]
        )
        print("Build successful, attempting to run")
    except:
        print("Something went wrong! EEK.")
    print("----------------------------------")
    print("Server build successful.")

    print("Creating container to run server...")
    print("----------------------------------")
    sp.Popen(
        [
            "docker",
            "run",
            "-it",
            "--name",
            CONT_SERVER_NAME,
            "-p",
            "8080:8080",
            "--rm",
            "--privileged",
            "-v",
            "{}:/mtriage".format(DIR_PATH),
            "{}:dev".format(SERVER_NAME),
        ],
        shell=False,
        stdin=None,
        stdout=None,
        stderr=None,
        close_fds=True,
    )
    print("----------------------------------")
    print("Server run successful.")

    print("Creating container to build viewer plugin...")
    print("----------------------------------")
    try:
        sp.call(
            [
                "docker",
                "build",
                "-t",
                "{}:dev".format(VIEWER_NAME),
                "-f",
                "src/build/viewer.Dockerfile",
                "src/lib/viewers/" + viewer,
            ]
        )
        print("Build successful, attempting to run")
    except:
        print("Something went wrong! EEK.")
    print("----------------------------------")
    print("Viewer plugin build successful.")

    print("Creating container to run viewer plugin...")
    print("----------------------------------")
    sp.call(
        [
            "docker",
            "run",
            "-it",
            "--name",
            CONT_VIEWER_NAME,
            "-p",
            "8081:80",
            "--rm",
            "--privileged",
            "-v",
            "{}:/mtriage".format(DIR_PATH),
            "{}:dev".format(VIEWER_NAME),
        ]
    )
    print("----------------------------------")
    print("Viewer plugin run successful")


if __name__ == "__main__":
    COMMANDS = {
        "build": build,
        "develop": develop,
        "test": test,
        "clean": clean,
        "viewer": viewer,
    }
    parser = argparse.ArgumentParser(description="mtriage dev scripts")
    parser.add_argument("command", choices=COMMANDS.keys())
    parser.add_argument("--input", "-i", help="Input Folder", required=False)
    parser.add_argument("--viewer", "-v", help="Viewer Plugin Folder", required=False)
    parser.add_argument("--gpu", action="store_true")

    args = parser.parse_args()
    cmd = COMMANDS[args.command]
    cmd(args)