## 03/06/19

I have experimented with manual manipulation of the 'field_recording' exemplar. The files rendered from scraping the harddrive come out at various lengths and have different experiential properties when looped. It's a simple way to create an intensive listening environment as one has to peer through the distortion/noise/glitches to the underlying behaviour of the sound.

Now considering how the computer might create chains of these samples and how it would decide to change the loop.

How can I expand the set of sounds to be greater, creating variety between iterations or perhaps more density. Just MORE selection properties and the possibility of creating greater transition

## 04/06/19

A system for boredom. Correlate?

## 07/06/19

Listening to various 'spines' that have emerged from the classification process I came across (by chance) the Live-files_34.db. Listening to the various cuts that were made I was intrigued how the original version sounded. It displays a somewhat random, broad and all over the shape behaviour but each slice in and of itself is quite interesting. How can I reorganise the slices? I feel compelled to try something like simulated annealing again to create a search pattern that can be sonified or otherwise accessed as an organisation structure.


## 01/08/19

Today I produced excellent results in creating conceptually coherent groupings using a more advanced and contemporary set of dimensionality reduction techniques.

The process is as follows.

1. Compute t-SNE dimensionality reduction using the script and associated yaml file. This produces a json file containing two dimensional coordinates for each file's position in a space
2. Run DBSCAN using the output of t-SNE as the input data. This produces a JSON file containing keys (clusters) and values(audio belonging to those clusters)
3. Use the cluster_explorer max patch to listen to the playback of samples within a cluster

I think that I find this interesting because I have taken a very dense and slow to navigate space and had the computer make quite close conceptual groupings out of material that has not necessarily been derived from the same data in the initial scraping process. It has allowed me to collect materials and organise them so that they have coherence. I can then disrupt this coherence or use it, but it gives me a more stable place to start from when approaching organisation and selection of materials.

Aesthetically, I am trying to create small pieces that are focused intensenly on a specific motif or material type. The clustering produces not only perceptually 'smooth' groupings giving me more technica manipulation/finesse/control/understanding of the entire data set, but is throwing at me groups which would otherwise take ages to collect. I am particularly interested in how these groupings might be filled with their own 'special features' as well as what might happen when I start to unpack the structures within the clusters either progrmatically, perceptually or using another control mechanism to turn it from a list of samples -> texture or stream of sound.

The large database in and of itself is not that interesting, but it is more interesting to disect the novel features of the space.

## 05/08/19

Clustering the more successful dimnesioanlity reduction data (TSNE and ISOMAP) works well in extracting perceptual groupings. DBSCAN is good at making close knit groups and is 'clever' in the sense that it picks the right amount of clusterss for you (there is no number_clusters parameter). Today I attempted Agglomerative Clustering which is a hierarchical method. I'm not sure the hierarchical aspect of it makes it much different, however, with this technique we specify a number of clusters for it to form. As it is hierarchical and a 'bottom up' approach it starts off with a high number of clusters spread out across the space and merges nearby groups together until it satisfies a given number of components. As a result there are strong perceptual groupings with some overlap between clusters that have been merged. DBSCAN originally returned 1638 clusters and so I provided the n_clusters parameter with approximately a third of this value (500 clusters) which has produced interesting groupings that show a higher degree of internal variance. My assumption is that by capping the n_clusters at 500, clusters that would otherwise be separated by something like DBSCAN get merged which offers the possibility of muddying the purity of each cluster. It would be good to see if the hierarchical data could be accessed to create a series of clustering 'layers', but this could be done by outputting results given different n_clusters paramaters.

After some basic experimentation with the groupings from the clusters in Max, i think that creating some way of understanding the relationship of clusters will give me the musical hierarchical control I want. That said, I think that there is the possibility of a miniature existing in taking the clusters at face value and iterating through them. In a more controlled manner I envisage the computer maximising envelopes at different temporal and perceptual levels. I should be able to determine the 'pitchiness' over time while controlling the amplitude selection of samples within that sustained pitchiness envelope.

## 13/08/19

Creating a space in which I can interrogate instinctual dislikes/likes/inclinations about the material.

A consideration: Do I need a low level way of manipulating patterns? Or should the algos just take care of ordering. I might just need better control over the algos themselves with parameter tuning and specificity.

**I think its time to let the aesthetics guide me a bit... the clustering is done...**

## 02/09/19

It will be important to discuss the machinations over analysis and how to produce meaningful descriptors. A story could be told showing how different descriptors fail to give some sort of clarity, and how dimensioanlity reduction on a set of more abstract data rendered more useful results. Again, the 'magic' of the computer transforming numbers into something else.

## 06/09/19

Today I worked extensively on fleshing out how each cluster functions and listening to the the behaviours that are produced by playing back the samples in arbitrary, stochastic ways. This went beyond just listening and labelling toward a process of trying to imagine compositional mechanisms and transformations that could be applied to each cluster within the Framework of a clustering hierarchy. 

An interesting occurance was that **after** making some more detailed notes on clusters which I thought had more long term compositional fruit, I went back and listened to some of the `short_spines` and went about looking which clusters they belonged to. On more than one occasion I found clusters that I was interested in contained spines I had selected much earlier and I think that this somehow gives validity to the use of dimensionality reduction and clustering to create hierarchies and groupings. 

## 09/09/19

Probabilities for playback using z12 are important. Achieving a distribution, and 'ordering' of the right elements can drastically change the overall feeling of the output.

I think that working with Max like a complex sequencer is not the way that I want to work. I am happy that the computer has created perceptual groupings for me, but I don't want to try and abstract away something that I want more fine control over (the organisation)

## 16/09/19

Today I focused on collecting audio from the larger set that was sonically relevant to the pitched material that I hand-organised previously. I started out motivated to increase the breadth of material with similar qualities - pitched, compressed, a sliver of noise to accompany high pitched tonal qualities.

Using NMF and the reascript interface to the FluCoMa tools I was able to create surgical separations of the noise content from the harmonic content in some of the files. This proved useful and something I may want to use more liberally on other files in the future or as a compositional mechanism.

I also started to form some longer term gestures ~30 seconds implementing the removal of noise through NMF. Some incredibly sparse sounds were formed as a result. 
Lastly, I found it useful to use specific files of interest as anchors and look for related material by observing how the clustering python scripts grouped other samples to these. One example chain of thinking here starts with `pos.dat_1.wav` which I know had a very similar sonic profile to the outputs of files created from the `.maxwave` extension. I then looked into the `AHC_250.json` cluster file to find that most of the `.maxwave` had been kept together in their own clusters and without any other material infiltrating - except for *cluster 54*. I began listening through each of the files in this cluster and referring back to their own segmented source material. I found some excellent material that I would otherwise not have come across, particularly in `3870112724rsegmnoittet-es.sqlite.wav`. This will probably spawn a new short track as well as provide me with some small snippets that I can cross pollenate the ideas with. 

## 18/09/19
- Cluster 19 contains segmoinette which contains references to KnowledgeC.db
- Cluster 62 contains segmoinette which contains references to Addressbook
- Cluster 64 contains segmoinette which contains references to 5353E668........wav
- Cluster 54 contains segmoinette which contains references to KnowledgeC.db.
- Cluster 120 contains segmoinette which contains Live-files-34.db.wav segments

## 11/10/19

Focusing the computer’s role toward a ‘computer-assisted’ one has helped me to take more conceptual risks, particularly with that of form and time. That said, the computer’s influence on these aspects of the music are not completely removed, rather, they exist in a more influential rather than controlling role. For example, the clusters themselves when concatenated in a completely simple and arbitrary fashion have determined the length of small loops that make up longer loops and layerings. The small pops, and clicks emergent in this process (enabled by the ReaScripts) has become a feature of the work - a process that is not uncommon in other creative practices. 

In another words, the computer acts as a provocateur and enabler and leverages modes of thinking and doing that I would otherwise be incapable of mimicking.
Polyrhythms by accident from overlapping different clusters which have been strung together.

## 17/10/19

Work is coming to a close on the soft rhythmic piece. I feel a lack of new ideas right now so that one is going on the backburner momentarily until something fresh comes up. More specifically, I feel held back creating new combinations of material that sustain interest, but this is possibly linked to a kind of listening that is not engendered well in studio 9... I think that there has to be more detailed, rhythmic interactions which can be created by mixing either lone clusters, or composite clusters together and the methods and processes which I have used for finding these previously have run dry. I am thinking of other ways I can generate sound from what is already a substantial set of audio and possible solution could be WaveNet. Something to investigate. Another aspect of composing this piece that is causing friction is how much processing is too much? I have started to manually apply several processing techniques already (filtering, speed alterations) but to an extent there is no evidence that these processes did not already exist in the output of the scraping process. 

Right now, the piece feels like it could also exist in a large speaker setting as a stereo or 3 channel piece diffused over a complex array of speakers and that whole avenue feels mostly unexplored.

## 18/10/19

IDEA: create a series of 'filler' works which use a unifying technique over a number of clusters. There are several groups which appeal to my sensibility of ordering and arranging a single stream of samples. Largely, the other works so far (pitched, danceabilityone, three-ideas) work with heavy layering, but something that attracted me to the sample set in the first place was the natural success of stringing together the audio files.

## 31/10/19

- Experimented with convolving samples together using multiconvolve. Works well, especially on the quieter stuff or with short impulses and long tonal files
- Composed some more.
    - I think that the impulse based composition is coming to a close.
- Transient separation is superior to high pass filtering when you want to create something 'clicky' and detailed. It makes it sound less 'lo-fi and scratchy' and focuses in on the delicate qualities of the sound.

## 18/12/19

What is it about my working method in REAPER that has made thinking algorithmically more creatively 'truthful'. I think it is the ability to iterate on ideas rather than to lose the once you press stop. When you automate out certain processes, like cycling through combinations of musical material, or groups of that material you never get to retain the state of what happened unless you build something that can do this. REAPER (and git to an extent) keep a trace of what has already been done so this allows you develop ideas without reverting back to the artefacts which are remnant from the creative process. When using Max, what is often left behind is the code itself and so you are always working from a patch which makes the sound, rather than from the sound itself. When REAPER leaves a trace this informs the next decision, while always having to code the next decision is onc removed from using your ears.

### thoughts on composing and what I **need** from technology

being able to combine and break apart material quickly is important to me - creating a chain of processing that can be traversed quickly

I thought that I was into intensely organised micro-structure, but actually I am more interested in not managing microstrucutre but rather dealing with these kind of texturised blocks of sound that can be pulled apart and put back together in new ways if need be. my interest in manual work is more to do on the meso and macro level of things in response to the serendipitous arrangement of blocks which is shaped by indeterminate micro-organisation. The rhythms in interrupt are not coming from any kind of relationship that I have to rhythm or a rhythmic strucutre but my ‘riffing’ on the random organisation of contiguous samples, and the layering of different streams of these samples.

what is most conducive is a kind of play in REAPER where I follow the chain


taking inspiration from unbuffered cluster exploration:

	- when samples are concatenated randomly, their homogeneity affects the musical function.
        - variegated groupings produce something that is less blocky and more of a constantly oscillating texture, like a kaleidoscope.
	    ⁃	the smaller the loop the more robotic and ‘synthesised’ it can sound
	    ⁃	Using the hierarchy of clusters you can flit between these ideas quite seemlessly and also do density interpolations by randomising contiguous segments of different distributions of each cluster.


### Reflection on today
Right now, the thing that is driving the music is your ears. What do you want to hear? Reflecting on today's composition session There needs to be a reconsideration of whwat it means to create blocks where two cluster blocks interact. The form is somewhat moving to a quite pulse oriented and call/answer mechanism to guide different bits of material. Perhaps it is about what happens in the gaps, and how long the gaps get. Maybe the gaps get super wide and the whole thing kind of 'unravels'.

How can modify the relationship between the three rhythmic streams that comprise the guts of the work. Initially I enhanced them by creating a hybrid stream and adding this to the original two. This thickened the texture, perhaps I just need to keep adding more in order to develop music. It might be the case that these 'guts' are all that I am listening to, and the other streams simply are weaving between the impulses. This might be an interesting conceptual route to take - whereby increasing space in the guts leaves room for more nuanced interruptions

## 20/12/19

The FluCoMa tools provide a useful for mechanism for exploration - another kind of response.. this one is sonic rather than organisation, pattern based.

Reperforming the same processing on an alreayd procesed file in order to make the algorithm search for things it has already 'found' but to also push it to its limits in a way that it finds things it is otherwise not designed to look for.


`one thing to develop in the next project is a highly controlled sense of microrhythm where I have more control`

There is a sense that there are parts of this that you want to feel like automata, and machine-like but it feels so heavily organised. There needs to be a committment made to either of these direcitons, and I think that *listening quietly*