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

## 4. Problem Statemens and Research Questions

Of late, learning factories seem to be finding place in most universities and a popular method on giving hands-on experience to students. A learning factory is a facility that realizes a process or product in an academic setting for the purpose of training and edu-cating students [5], normally in or in close proximity to the campus premises. They are set up with the intention to inspire action-oriented experiential learning [2][6][7][1]. 
However, Some of the limitations of the learning factories identified are as follows [5]:
  * Limited mapping ability for challenges prevalent in academia and industry as learning factories generally focus on particular aspects of manufacturing.
  *	Space and cost related issues when it comes to mapping the different factory levels.
  *	Time required to complete production orders having a high cycle time.
  *	Fixed locations of learning factories mean limited mobility.
  *	Evaluation of production related competencies after the learning experience.

Assisted learning via digital twins aims to support student in education process grasping, understanding and applying new ideas. Digital twins are seen as an environment, where the learning process can be facilitated. In order to support student, the ‘digital assistant’ has to have some representation of learning objectives and feedback from and to the student to guide her or him towards set objectives. Such a system should be able to evaluate and compare performance of different students. These gives a rise to the fol-lowing research questions:

  *	RQ1: How digital twins in an academic set up can augment the learning experi-ence and how it can mitigate the limitations of learning factories?
  *	RQ2: What is a systematic approach to develop such a digital twin?
  *	RQ3: How to model learning outcomes in context of digital twins?
  *	RQ4: How to evaluate performance of the students?
  *	RQ5: How to guide a student towards desired level of skills with respect to her/his current status?



## 5. Research Methodology

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

### 5.6 Scale the Twin

<a href="https://drive.google.com/uc?export=view&id=1qNBpyNiUsyXrqQv7HX5ZAMs2nw411Flc"><img src="https://drive.google.com/uc?export=view&id=1qNBpyNiUsyXrqQv7HX5ZAMs2nw411Flc" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>

The digital twin is scaled to encompass the entire layout. The modular ap-proach to developing the pilot twin meant that this stage involved only duplicating ex-isting components as the pilot twin constituted of a component of each type in the com-plete layout. 

## 6. Implementation

This chapter presents the concrete work done in regard with development of the digital twin in the study

### 6.1 System Architecture

#### 6.1.1 The manufacturing System

The Manufacturing Control System consists of hardware and software components. The hardware consists of a controller that functions as the brain of the system an interface between the Digital Twin and the physical system. The control cabinet is often integrat-ed with a control station. The Manufacturing Control System software components in-clude:

*	A control system simulator representing the physical system that exchanges su-pervisory statuses and control commands with the controller. 
*	A web based interface known as the Data Manager that is used to manage mas-ter data relating to part routing and manufacturing, make and visualize orders and schedules and view production logs. 
*	A web based Dashboard that shows real-time 3D view of the system with live status updates about devices and operational conditions.

There exists two conﬁgurations in which this system exists; virtual and physical. For the purpose of classroom or distance learning, there exists a virtual conﬁguration devoid of the simulator and the controller, where the Digital Twin can be operated without the physical FMS environment. Although the sense of a Digital Twin is arguably lost here by deﬁnition due to the absence of it physical counterpart, it models the controller pre-cisely as the manufacturing control system hardware. The high maturity in modelling the control system means that for all purposes of discussion the sense of a Digital Twin is still maintained. This virtual conﬁguration is being leveraged to train personnel and edu-cate pupils of the concept of the FM System before actually working on the physical system. In this virtual conﬁguration the Control Station interface from the physical sys-tem, i.e. the Dashboard and the Data Manager, is made available on via a web browser and it is this configuration that we make use of in this study.

#### 6.1.2 Implementation Architecture

<a href="https://drive.google.com/uc?export=view&id=1M58af8LtgPA3F0E7G1t8IGt6rMvdwo0Z"><img src="https://drive.google.com/uc?export=view&id=1M58af8LtgPA3F0E7G1t8IGt6rMvdwo0Z" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>

The system architecture (depicted in Figure 23) consists of the Digital Twin of a manu-facturing system that interacts with its users (both students and teachers), a knowledge base that consists of the domain ontology. A reasoner engine assesses the learning out-come of the student against the set learning objectives and constantly evaluates the pro-gress of the student towards the set objectives with prior defined rules. The Observer (not implemented in the use case) is the module responsible for capturing additional in-formation that pertains to the user behaviour and thereafter updates the learner’s profile. This could be anything from mouse tracking, eye-tracking, time spent navigating the digital twin and so on.

### 6.2 Ontology Modelling

Ontologies have long been used for representing information. We use ontological mod-els of the domain knowledge and other knowledge facets in the digital twin environ-ment. The ontology developed comprises of three main artefacts as a sub class of the general class Thing; the manufacturing system, the pedagogical elements and the learn-ing that occurs as a result of pedagogy. 

#### 6.2.1 Manufacturing System Ontology

Representation of the manufacturing system is created using ontologies as shown in the figure below. As can be observed, the manufacturing management system is not modelled in its entirety with the aim to keep things simple. Rather, only those domain information relevant to the context of the learning use case has been modelled in detail while remain-ing facets have been modelled without any detail at all.


<a href="https://drive.google.com/uc?export=view&id=1DCAOUvA_JLOYR2RgTUxPmW-7om4QnbxZ"><img src="https://drive.google.com/uc?export=view&id=1DCAOUvA_JLOYR2RgTUxPmW-7om4QnbxZ" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>

Of importance in the domain information is the Manufacturing Control System Data Manager. It consists, inter alia, the Master Data and Production details. The Production Class mainly consists of the orders, that has hasOrderID, hasQty, hasOrderDescription, hasOrderStatus as data properties and hasPart as an object property that has Class Part_Master_Data as its range.
 The part master data consists of the Part Master Data and the Fixture. The parts have data properties hasPartDescription, isPartType, hasPartName, hasPartID while has an object property hasOperations of range Operation. Operation itself consists of data properties hasFixture, hasOperationID, hasOperationName and object property hasOp-erationProcessSteps of range Process. Process further has data properties hasPro-cessStepName, hasProcessProgram, hasProcessID and hasProcessAllowedDevices.
The structure underlying the ontology mentioned above is that the Order class has one or more orders (instances of class Order) that contain a part. Each part is manufactured by one or more operations (instances of class Operation). These operations further are materialized by a sequence of process steps (instances of class Process) that include a combination of loading, machining, washing, manual and unloading steps.	

#### 6.2.2 The Learning Ontology

<a href="https://drive.google.com/uc?export=view&id=1Y57577ar9PLYAB4USnTSSWxNineNbiHD"><img src="https://drive.google.com/uc?export=view&id=1Y57577ar9PLYAB4USnTSSWxNineNbiHD" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>


The learning ontology (super class Learning) comprises of the learning outcomes, learn-ing objectives and the learning taxonomy (Figure 25). The LearningObjectives class represents the ABCD model (Section 2.5.2). Hence, it comprises of properties hasAudience, hasBehaviour, hasCondition and hasDegree. 

The LearningTaxonomy Class represents the SOLO Taxonomy and has a property hasLelvel that denotes the taxonomy level.
The LearningOutcomes Class represents the outcome of learning and is modelled to have two properties, hasAssessment and hasSOLOLevel.

#### 6.2.3 Pedagogy Ontology

<a href="https://drive.google.com/uc?export=view&id=1TFsl6vD8ndXcmvqq5R7FwYyMD5Ec-xdV"><img src="https://drive.google.com/uc?export=view&id=1TFsl6vD8ndXcmvqq5R7FwYyMD5Ec-xdV" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>


The pedagogy ontology onsists of Class Person and Class Course. The Person Class constitutes of sub-Class Teacher that teaches (object property) a Course and a sub-Class Student that studies (object property) the Course.

#### 6.2.4 Domain + Manufacturing + Pedagogy: The Combined Ontology and Course Alignment

<a href="https://drive.google.com/uc?export=view&id=1HmJUzgWlzjbkxG-FVCSHrzj-WDmAGs-I"><img src="https://drive.google.com/uc?export=view&id=1HmJUzgWlzjbkxG-FVCSHrzj-WDmAGs-I" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>


The combined ontology is a merger of the above three ontologies representing the manufacturing system, pedagogy and the learning that occurs within the domain. The main objective of this merger is the alignment of the course, and by doing so mak-ing sure that the course objectives (and thereby the course goals) are in harmony with the learning activities and the assessment.
This merger makes way for a few associations. These associations are marked in red. A student that takes the course hasLearningOutcome (object property) of Class Learn-ingOutcome. The course hasCourseObjectives (object property) of  Class Learn-ingObjectives which inturn hasAudience as the student. The LearningObjectives Class also has an object property hasBehaviour that for the current use case is modelled as Class Order. Class Order is also modelled as the learning outcome that has hasAssessment which in the context of this use case is the Order Class of the Manufacturing Management System. 


### 6.3 Digital Twin Component Design in Visual Components

#### 6.3.1 Material Station

#### Functioning Logic

The material station is where materials required to be loaded on machining pallet is brought on material pallets. The material station has two doors, one on the operator side and the other on this aisle side. The aisleDoorOperate signal is triggered by the crane when it is assigned a task to either pick from or place to the material station a pallet. The material station has two ray cast sensors that detect when the material pallet has reached either ends of the conveyor.
Once the pallet is placed and the crane has retracted its forks, the aisleDoorOperate is signaled a False value by the crane to close the Aisle door. Once the pallet is inside and the aisle door has closed, the operator door opens. Once the operator door has opened completely, the material pallet is carried forward on the conveyor towards the operator. Once the material pallet reached the operator end, it triggers the Operator Raycast Sen-sor that causes it to stop the conveyor.
Once the machining pallet is “loaded” in the corresponding Loading Station (value of RefNode Property, see in Footnote 7), the material station sends the material pallet backwards towards the aisle. The Operator Door closes and the Aisle Door opens once the material pallet has reached the Aisle Side.

#### 6.3.2 Loading Station

#### Functioning Logic

The Loading Station is used to load machining pallets. It has two doors, the Aisle Door, just like the Material Station and the operator door, that unlike that of the material sta-tion, swivels on hinges. The aisleDoorOperate signal is triggered by the crane when it is assigned a task to either pick from or place to the loading station a pallet. This causes the Aisle Door to open.
Once the pallet is placed and the crane has retracted its forks, the aisleDoorOperate is signaled a False value by the crane to close the Aisle door. Once the pallet is inside and the aisle door has closed, the operator door opens. 
After the machining pallet has been loaded, the operator door is closed first, followed by the opening of the aisle door.


#### 6.3.3 Machining Centre

#### Functioning Logic

The machining center processes the machining pallets. The machining center has the AisleDoor door the opens to the aisle. . The aisleDoorOperate signal is triggered by the crane when it is assigned a task to either pick from or place to the machining center a machining pallet. This causes the Aisle Door to open.
	 

Each machining center is such that it has two pallet holders (A and B). At any given time, the machining center can have one of two statuses, either “ASideOut” or “BSideOut”, or might be in the process of changing between these two statuses. “ASideOut” means that the pallet holder A is out, while “BSideOut” means that the pallet holder B is out. The pallet holder that is out is called the Changer while that what’s inside is known as the Table. Hence, when the machining center is in the “ASideOut” status, it the pallet holder A is the changer and B the table and vice-versa

Once the machining center receives a pallet in the pallet changer, it executes all the re-quired NC programs. The rotation of the pallet holders, and thus the changing of the status of the machining center is also a program known as “PalletChange.nc”. Some-times, the machining center may tend to skip out on NC programs that are to be execut-ed on the machining center due to its delay of arrival to the machining center. To avoid this, a TaskScheduler is implemented (as shown in Figure 34) that records all the tasks in real-time from the simulator and makes sure its carried out once the pallet arrives, alt-hough needless to say, if the pallet already has arrived on time it NC Programs are exe-cuted immediately. 

#### 6.3.4 Crane

#### Functioning Logic

The crane is modelled as a robot whose workspace is the storage area. The crane queries the Manufacturing Control System Simulator for active tasks repeatedly. It may be such that the crane in the simulator finishes tasks at a very rapid pace due to less visual fideli-ty in the control system web interface. This means that if the crane in the VC model only performs the current active tasks, it is likely to skip tasks from the control system Simulator if the crane there (in the Simulator) gets too far ahead. 
For this reason a script called TaskScheduler is added to communicate real-time with the control system Simulator and schedules tasks for the Crane in the VC model. The script architecture is similar to that of the machining center shown in the figure

#### 6.3.7 Completed Layout

<a href="https://drive.google.com/uc?export=view&id=195awnwMTpAIbwXsEbUt34JXsGJ08ZLPA"><img src="https://drive.google.com/uc?export=view&id=195awnwMTpAIbwXsEbUt34JXsGJ08ZLPA" style="width: 500px; max-width: 100%; height: auto" title="Click for the larger version." /></a>




