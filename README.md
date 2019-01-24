# Leveraging Digital Twins for Assisted Learning of Flexible Manufacturing Systems

## 1. Abstract
Learning Factories provide a propitious learning environment for nurturing production related competencies. However, several problems continue to plague their widespread adoption. Further assessment of attained competencies continue to remain a concern.
This study proposes the use of digital twins as an alternative. An iterative research methodology towards modelling a pedagogic digital twin is undertaken to build a learn-ing environment that is characterized by ontologies that model learning objectives, learn-ing outcomes and assessment of the said outcomes. This environment facilitates auto-mated assessment of the learner via ontological reasoning mechanisms. The underlying schema takes into account the learner’s proﬁle and focuses on competency attainment through reasoning of behavioural assessment of aligned learning outcomes.
The work presents also a case study that demonstrates how the learner’s competency level may be evaluated and compared with other learners thus warranting its use a learn-ing tool that proves beneficial in an academic setting.

## 2. Software Environment
* Programming Language: Python
* Query Language: SPARQL
* Domain Information Representation: Web Ontology Language(OWL)
* SPARQL Endpoint: Apache Jena Fuseki Server
* Ontology Development: Protege
* Digital Twin Platform: Visual Components

## 3. Physical Environment

A flexible manufacturing  system located in the premises of its vendor


## 4. Research Methodology

This chapter aims to contribute with the methodology used in the development of the digital twin in the thesis.The subsections guide the reader into systematic iterative steps adopted by the author in studying the research problem along with creation of the digital twin.


<a href="https://drive.google.com/uc?export=view&id=11ZQWlRw9jkyzrS4qzSvFePwmO-JVgg8M"><img src="https://drive.google.com/uc?export=view&id=11ZQWlRw9jkyzrS4qzSvFePwmO-JVgg8M" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>

### 5.1 Envisage and Envision

This stage involved researching the aptness of Digital Twin in the educational set up by examining the value it brings to the students. As part of the research done, two publica-tions emerged. 
In the first Publication titled “Leveraging Digital Twins for Assisted Learning of Flexible Manufacturing Systems” an approach in using Digital Twin as a medium for educating students on (ﬂexible) manufacturing systems is presented based on a pedagogically sound framework, i.e. Kolb’s experiential learning cycle. The transformation of a general hypothesis to competency development during different stages of the learning method-ology is adjacently compared with Kolb’s experiential learning to justify the proposition.
The second Publication Titled “Learning Experiences Involving Digital Twins” present-ed widely researched learning (behavioural, cognitive and humanistic) theories were presented before using them to draw a parallel to a learning framework developed in the earlier publication. In doing so, an attempt was made for warranting its use as a tool to educate students.
At this stage the learning outcome of the existing course were identified as “Ymmärtää tuotannollisen toiminnan perusteet, tärkeimmät valmistustekniikat ja toimintamallit su-omalaisessa teollisuudessa” or as  “Understand the basics of production activity, key manufacturing techniques and operating models in Finnish industry” in English.
This stage, while laying the foundations of the research also gave the green light to pur-sue solutions to the posed research questions.

### 5.2 Identification of the Process and Course Activities

This stage involved finding out the right process and layout that would help in accom-plishing the course objectives. The manufacturing process chosen was that of a ﬂexible manufacturing system and understanding its principles were the objectives. The configu-ration layout was ascertained after multiple discussions and negotiations with course personnel and the supplier of the manufacturing system until a configuration layout was mutually agreed upon.
Some of the factors taken into account (besides the ones that are typical of FM Systems) during identiﬁcation of the conﬁguration were as follows:
•	The number of loading stations should be enough to accommodate at least five groups at a time taking into account the number of course participants.
•	Distributing the loading and material stations to prevent cramping as it would be unsafe to as people and forklifts would be in the same place. Although a virtual system, safety standards were not to be violated.
•	The processes and thereby the machines that are incorporated should be broad enough for students to comprehend those important practices prevalent in the industry.

The Layout drafted in CAD at this stage is shown in Figure.

<a href="https://drive.google.com/uc?export=view&id=13g-8cnM8q5PRbvjfEJIVM9Yw5ePdG4Cm"><img src="https://drive.google.com/uc?export=view&id=13g-8cnM8q5PRbvjfEJIVM9Yw5ePdG4Cm" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>

The layout consisted of an Automated Storage and Retrieval System that included a crane and a storage that could house 126 pallets (84 machine and 42 material pallets), five Loading Stations, six Machining Centers and two Material Stations. 
The course was set to follow the didactic framework developed **in the Chapter 3, Sec-tion 3.1**. The lectures are planned to introduce the course to the student while explaining theoretical concepts underpinning flexible manufacturing systems. The digital twin is introduced here. This is to be followed by an online quiz where the students would have to answer questions such as “Where can I find information about the remaining life on this tool?” The goal of this exercise is to familiarize the students with the user interface and the ideology behind it.
The next part of the didactic framework takes place in the laboratory where in the labor-atory where the students were to focus mostly on the non-physical side of the system and create a fixture, a part, install the fixtures on a pallet and then make an order. The required NC-programs and materials will already be present and the students are al-lowed to use them. This was done so as to save time considering the number of students taking the course. 
This was to be followed by an exercise at the Training Center. In the second exercise, the students will now manufacture and complete the order they made in the first exer-cise. The main focus here is the physical aspect of the system such as installing the fix-tures, adding material to the fixture and seeing the material getting machined and moved in the system and actually using the loading stations.


### 5.3	Pilot a Twin

A pilot twin is next developed consisting of a component of each type (Figure 21). Dur-ing the development of the twin, several design principles (covered in Section 5.1) were followed. Of this, modularity is of prime significance and is worth a mention here. The pilot twin was realized with each component having logic necessary only for its own functioning. In other words, there is no central middle-ware that takes care of the func-tioning of other components. This was part of a vision of the digital twin to be able to adapt to various layout configurations as part of future work to the work done in the thesis. 
Known performance related issues with prior implementation necessitated to be vigilant in this regard. Several steps were taken in this regard.
1.	The number of simultaneously running python scripts were kept to a minimum in each component. The same is the case with other behaviors and properties
2.	Features of components were “collapsed” and “merged” so as to have lesser geometries to be tracked in real-time while the simulation is running,
3.	Raycast sensors used to detect  the presence of pallets on conveyors were acti-vated only if there was an incoming pallet to the station rather than to have it run throughout. 
4.	Services were selected carefully only to serve their required purpose. For exam-ple, services that enabled to obtain the location of pallets in particular positions were invoked by components checking if there were pallets in only their respec-tive containers rather that invoking services that provided location details of all pallets.

<a href="https://drive.google.com/uc?export=view&id=1Hf9LPaTuLNGnmeoLROq1DofZjIZ4pHf8"><img src="https://drive.google.com/uc?export=view&id=1Hf9LPaTuLNGnmeoLROq1DofZjIZ4pHf8" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>

### 5.4	Deploy Pilot Twin

The Pilot twin is deployed and what followed the deployment is a number optimizations in performance parameters tuning to get it to the desired state. This deployment serves mainly two purposes:
1.	Checking how the deployment has supported the goals identiﬁed as a part of the envision and modelling stages is analyzed. 
2.	The deployment of the pilot twin also serves as a midway point in implementing the functional logic in the creation of the digital twin. 
Since the next step would be to scale twin to encompass the complete layout any anomalies present would be duplicated and it would be appropriate to rectify any pre-sent at this stage. Commenting source codes using software design styles and conventions was also done in this stage so as to avoid re-commenting similar codes once scaling the twin to the complete layout.

### 5.5 Model Domain Knowledge and Pedagogic Extensions

As mentioned in the earlier section, any digital twin of pedagogic value needs to have didactic transformations that justifies its pedagogical context of usage. Such transfor-mations, as mentioned in the research questions in the previous section, needs to have a description of the learning objectives. Further, any pedagogic tool would be incomplete without assessing and evaluation of the learning outcomes.
A discussion between ontologies and databases was presented earlier in this paper. However, the author has chosen to go ahead with ontologies for the following reasons:
•	Taxonomic reasoning was fundamental in deciding with ontologies due to their ability for semantic modelling of concepts. With the ability to use classes, prop-erties, instances, aggregation and generalization relations, ontologies were deemed more suitable as opposed to databases that focus on data storage and prove challenging to represent manufacturing domain knowledge. 
•	The Open World Assumption (OWA) by ontologies would prove useful in times when modelling the knowledge acquired by the students 
•	Ontology Query Languages such as SPARQL or SERQL uses rich vocabulary of the ontology via predicates. 
•	Future developments on works presented in this paper can be made with the on-tology developed in this paper. Using databases, it would be relatively difficult to build on existing databases and a new one would have to be built from the ground up.

### Scale the Twin

<a href="https://drive.google.com/uc?export=view&id=1qNBpyNiUsyXrqQv7HX5ZAMs2nw411Flc"><img src="https://drive.google.com/uc?export=view&id=1qNBpyNiUsyXrqQv7HX5ZAMs2nw411Flc" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>

The digital twin is scaled to encompass the entire layout. The modular ap-proach to developing the pilot twin meant that this stage involved only duplicating ex-isting components as the pilot twin constituted of a component of each type in the com-plete layout. 
