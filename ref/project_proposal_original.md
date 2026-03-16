This tab is for the project on ‘Steering Models Towards Safer Reasoning’.

## Research Objectives & Summary

On this page, you will be asked to provide details on your Research Objectives & Summary. This section outlines the problem you aim to address, your key research objectives, and the overall rationale for your project.

Questions marked with an asterisk (\*) are mandatory and must be answered. 

Guidance: We recommend 400-800 words for this section

* Research Statement (note: this was autofilled with the EOI statement)  
  * Provide a clear description of the problem or question your research will address and explain why it matters in the context of safe and secure development of AI systems. The statement should not exceed 500 words.

Building on recent work (https://arxiv.org/abs/2506.18167, https://arxiv.org/abs/2409.14026, https://arxiv.org/abs/2510.07364), we aim to do further research on steering reasoning to be more faithful and aligned, situated against a baseline of supervised fine-tuning and SFT combined with steering. In particular, Venhoff et al. (link needed) demonstrate the feasibility of steering reasoning capabilities and show that training a steering vector to mimic thinking-level-reasoning traces makes base models more pedagogical, producing discursive, conversational expositions with fuller explanations rather than merely increasing verbosity.

We will investigate several methods, including traditional steering vectors and activation addition (https://arxiv.org/abs/2308.10248), attention boosting (https://arxiv.org/abs/2506.13734), and manifold steering for long context reasoning traces (http://arxiv.org/abs/2505.22411). Other recent work (https://arxiv.org/abs/2507.22928) investigated CoT behavior with mechanistic interpretability techniques, potentially showing ways to use standard steering methods in a more targeted fashion. As a guiding metric for chain of thought monitorability, we will evaluate our models against an upcoming monitorability benchmark by the main author of this proposal.

We’re interested in trying many of the above techniques, because our hypothesis is that subtler behaviors in long context scenarios, such as faithfulness, will be unlikely to be steerable through traditional methods since those behaviors may be poorly represented by linear features, i.e., the Linear Representation Hypothesis (LRH) may not hold (https://arxiv.org/abs/2311.03658). This is supported by recent works which have found latent manifolds within activation space that better represent features than single directions do (https://arxiv.org/abs/2405.14860, https://arxiv.org/abs/2506.10920). Additionally, some works (https://arxiv.org/abs/2411.04430) have shown that sometimes prompting alone can lead to good behavior change without harming coherence of the generated text. Therefore, we will include prompting as a simple baseline and use this first before moving to more complicated white-box approaches.

To create our steering vectors, we will create many contrastive pairs of faithful and unfaithful reasoning traces. Under current faithfulness metrics (https://arxiv.org/abs/2505.05410), this is as simple as creating synthetic traces that do and do not contain the cue, and using the upcoming monitorability benchmark this can also be done in a more granular way to target different levels of reasoning verbosity. Since faithful reasoning is not always found ‘in the wild’ (https://arxiv.org/abs/2503.08679), we will create these reasoning pairs synthetically. From these pairs, we will conduct SFT on the aligned, faithful reasoning traces as our baseline, similarly to recent work on verbalization fine-tuning (https://arxiv.org/abs/2506.22777) . We will also attempt steering our fine-tuned models to test whether a combination of both methods will lead to higher outcomes than either alone. 

This work will constitute the core of our proposal, and we expect will take the majority of the allotted time. Conditional on time and funding, we will also extend our steering efforts towards latent reasoning models such as COCONUT (https://arxiv.org/abs/2412.06769). Steering in this instance could be done on the latent vector that substitutes for the next token in reasoning rollouts, by investigating structural differences in latent communication between more or less capable models, or more, against a baseline of directly interpreting the neuralese itself through detokenization.

This project intersects with all CoT monitoring research areas, principally the ‘Chain-of-Thought Monitoring’ subsection of the ‘Empirical Investigations …’ area. We tackle the combination of white box methods and monitoring of reasoning traces, meaning that our work also touches on the ‘Interpretability’ research area as well, and the ‘Benchmark Design’ area regarding CoT reliability and misalignment modes such as steganography and unfaithfulness to its internal reasoning.

* Key Research Objectives (400-800 words)  
  * List the specific research objective(s) that the project will achieve.

We propose the following research objectives:

1. Creation of a dataset of aligned and misaligned reasoning patterns  
   1. This dataset will be necessary for training our classifiers well, and would be tagged not just with binary labels, but with tags per section and behavior, such as backtracking behaviors.  
   2. Some work provides datasets of reasoning traces for safety training ([https://arxiv.org/abs/2508.20151](https://arxiv.org/abs/2508.20151)), we will use such prior work as constituent datasets and augment them with finer grained labels or synthetically created traces of our own design.  
2. Strong baselines for reasoning behavior  
   1. Prompting baselines: Here we want to thoroughly iterate on different prompts to induce the type of reasoning we expect to see. Some works ([https://arxiv.org/abs/2411.04430](https://arxiv.org/abs/2411.04430)) have shown good prompting techniques that do not diminish output coherence, which we will adopt.   
   2. SFT baselines: We’ll finetune on the aligned reasoning traces from the first research objective, similar to recent work on verbalization fine-tuning ([https://arxiv.org/abs/2506.22777](https://arxiv.org/abs/2506.22777)). Both this baseline and the one above will also be used in conjunction with any steering techniques we find signal with, since steering alone may be worse than either.  
3. Reasoning steering techniques   
   1. Building on previous work regarding steering reasoning models ([https://arxiv.org/abs/2506.18167](https://arxiv.org/abs/2506.18167), [https://arxiv.org/abs/2409.14026](https://arxiv.org/abs/2409.14026)), we aim to do further research to target subtler behaviors and misalignment modes such as lack of transparency or unfaithful reasoning. Our core hypothesis is that latent space structures for long context scenarios are unlikely to be straightforwardly linear, i.e. the Linear Representation Hypothesis (LRH) does not hold ([https://arxiv.org/abs/2311.03658](https://arxiv.org/abs/2311.03658)). Therefore, we will begin with investigating standard activation steering approaches ([https://arxiv.org/abs/2308.10248](https://arxiv.org/abs/2308.10248)), and move on to more recent techniques such as manifold steering ([http://arxiv.org/abs/2505.22411](http://arxiv.org/abs/2505.22411)).   
   2. We will also try additional work such as attention boosting ([https://arxiv.org/abs/2506.13734](https://arxiv.org/abs/2506.13734)), which is not strictly steering work but also broadly falls under representation engineering approaches.  
4.   Latent space reasoning control techniques  
   1. Farther along our proposed timeline, we are planning to extend our work to latent reasoning models, such as COCONUT or CODI ([https://arxiv.org/abs/2412.06769](https://arxiv.org/abs/2412.06769), [https://arxiv.org/abs/2502.21074](https://arxiv.org/abs/2502.21074)). Steering in this instance could be done on the latent vector that substitutes for the next token in reasoning rollouts, by investigating structural differences in latent communication between more or less capable models, or more, against a baseline of directly interpreting the neuralese itself through detokenization.  
   2. Our objective is to make some preliminary investigations here, but given that this would be farther down the line it is difficult to make things too specific given how many advances may be released. 

* Research Contribution (400-800 words)  
  * Briefly describe how your project will contribute to advancing knowledge or practice in AI safety and security. Include how it relates to The Alignment Project's research priorities. 

We anticipate that our work will advance AI safety broadly in several ways:

1. The release of detailed and well annotated safety datasets will enable a great deal of downstream research on safer reasoning. This future work doesn’t need to be focused on steering or other control techniques, and could instead be focused on post-training, activation monitoring, etc.  
2. Our techniques for steering, as well as the SFT and prompting baselines that we release, will be a valuable update to the community on which ways of controlling reasoning are the most effective. This information will help developers and labs understand the ways that they can better control reasoning at inference, in conjunction with current methods such as SFT on distilled traces and output only RL post training.  
   1. Since our aim is to understand and control reasoning behavior at inference time, this applies to the ‘Chain-of-thought monitoring’ subsection of the ‘Empirical investigations into AI monitoring and red teaming’ AISI research priority area. Because our work also relies on white-box methods, it also touches on the ‘Interpretability’ and ‘Benchmark design’ research priority areas.  
3. On a broader, ‘science of machine learning’ perspective, our work will be helpful to understand how reasoning structures emerge in latent space, especially so if we apply our methods to suites of open science reasoning models with training checkpoints (LMent: [https://arxiv.org/abs/2509.03405](https://arxiv.org/abs/2509.03405); Apertus: [https://arxiv.org/abs/2509.14233](https://arxiv.org/abs/2509.14233)). Connecting these results to new advances in latent reasoning models is also a core part of our grant application (see the work plan), where we will develop better control and monitoring methods in latent space.

## Proposed Methodology

This section should explain how you plan to carry out the research and justify your chosen approach.

Questions marked with an asterisk (\*) are mandatory and must be answered.

Guidance: We suggest using 400-800 words for this section.

* Research Approach (400-800 words)  
  * Outline your research design, methods, and the rationale for choosing them.

Here we answer some of the ‘why’ behind our proposal. For specifics about techniques, datasets, etc., please see other answers.

**Dataset construction** is necessary because we want very carefully tagged datasets for faithfulness and cue mentions. Even those datasets which have been released since the deadline for the first round of this application on Sept. 10th ([https://arxiv.org/abs/2508.20151](https://arxiv.org/abs/2508.20151), [https://metr.org/blog/2025-10-14-malt-dataset-of-natural-and-prompted-behaviors/](https://metr.org/blog/2025-10-14-malt-dataset-of-natural-and-prompted-behaviors/)) do not include tags for chain of thought faithfulness scenarios.

**CoT Faithfulness as the core experimental paradigm** was chosen because we can focus on explicit cue mentions as a simple addition to a long context reasoning trace. If we can steer on small subsections of the reasoning trace, we can better validate our findings and move towards steering of subtler behaviors over the whole context, such as sandbagging. We also choose CoT faithfulness work due to expertise among the team.

**Impacts of the current research** will include many aspects. General updating of the community on steering reasoning models, even beyond the reasoning steering research recently published by team members ([https://arxiv.org/abs/2506.18167](https://arxiv.org/abs/2506.18167), [https://arxiv.org/abs/2503.08679](https://arxiv.org/abs/2503.08679)), will help to inform about the best ways to understand and control reasoning behavior. Additionally, by comparing steering against strong prompting and SFT baselines, we can test whether steering is the best tool for the job, or if it works well in conjunction with some other techniques that we propose. And lastly, by testing for the ability to induce more faithful and transparent reasoning models across our method and baseline methods, we will better advance all safety agendas that rely on CoT monitoring as a defensive component.  

* Data Sources and Collection (400-800 words)  
  * Explain the type of data you will use or generate, how it will be collected, and any data access arrangements.

Our dataset will primarily consist of the reasoning traces that we build on and tag ourselves. There have been some recent releases of annotated reasoning rollouts for safety and refusal training ([https://arxiv.org/abs/2508.20151](https://arxiv.org/abs/2508.20151), [https://metr.org/blog/2025-10-14-malt-dataset-of-natural-and-prompted-behaviors/](https://metr.org/blog/2025-10-14-malt-dataset-of-natural-and-prompted-behaviors/)), as well as papers that discuss sentence-level tagging methods ([https://arxiv.org/abs/2510.07364](https://arxiv.org/abs/2510.07364)). Building on these advances, we will create ones with plentiful annotations for misaligned reasoning at a sentence-level.

For our core experiments, we work within the CoT faithfulness paradigm ([https://arxiv.org/abs/2305.04388](https://arxiv.org/abs/2305.04388), [https://arxiv.org/abs/2505.05410](https://arxiv.org/abs/2505.05410), [https://arxiv.org/abs/2501.08156](https://arxiv.org/abs/2501.08156)), where we will be looking for cue mentions within the dataset. To build this dataset, we will use LLMs as judges to mark cue mentions, since they are unlikely to form a natural cluster in latent space that an SAE could learn easily, as in ([https://arxiv.org/abs/2510.07364](https://arxiv.org/abs/2510.07364)). Since faithful reasoning is still difficult to find ‘in the wild’ ([https://arxiv.org/abs/2503.08679](https://arxiv.org/abs/2503.08679)), these traces will be synthetic rollouts created through a judge pipeline. 

* Analysis Methods (400-800 words)  
  * Describe how you will analyse data or validate findings, including any modelling or evaluation techniques.

Our core experimental paradigm will focus on CoT (un)faithfulness and monitorability metrics, under current development by the main author of this proposal. This means that increasing monitorability will be our main evaluation metric. We will additionally validate instance-level faithfulness using FaithCoT-Bench (https://arxiv.org/abs/2510.04040v1), which provides fine-grained labels of (un)faithful CoT steps and lets us check that our monitor aligns with per-instance truthfulness of reasoning traces.

We will additionally work on evaluating our models against different types of misalignment modes, such as deception or sandbagging, but will use CoT faithfulness metrics as our primary metric. For honesty vs. accuracy, we will use MASK (https://arxiv.org/abs/2503.03750) to measure whether models’ statements match their beliefs independent of factual accuracy; for overt deception, we will use DeceptionBench (https://arxiv.org/abs/2510.15501) to elicit and score real-world deceptive behaviors; and for power-seeking/oversight-avoidance trade-offs, we will report reward–ethics metrics on MACHIAVELLI (https://arxiv.org/abs/2304.03279). 

Finally, evaluation methods for latent reasoning models are still speculative given the lack of visible CoT. Some of our later work will focus on building better evaluation methods for these models, including adapting outcome-level endpoints from MACHIAVELLI (https://arxiv.org/abs/2304.03279), honesty/deception endpoints from MASK (https://arxiv.org/abs/2503.03750) and DeceptionBench (https://arxiv.org/abs/2510.15501), and stress-testing synthetic or externally generated rationales against FaithCoT-Bench’s instance-level labels ([https://arxiv.org/abs/2510.04040v1](https://arxiv.org/abs/2510.04040v1)).

* Cloud Service Credits Required (optional)  
  * Give a rough range (e.g. 90% confidence interval) for the value of AWS cloud service credits required, and briefly describe what these will be used for. As well as compute, these can be used for storage and data transfer.

N/A \- note I made some last minute changes to include this because of different grant funding sources for AWS credits

## Funding Information

On this page you will be required to enter details of the budget for your proposed research project.

Questions marked with an asterisk (\*) are mandatory and must be answered.

**Funding Information**   
The following funding table has been pre-populated with items under each budget heading. You can remove unused rows using the Remove Item button (Rubbish/bin icon). You can add additional items using the Add a New Item button.

For non-UK applicants, all costs must be converted to GBP using the exchange rate published on the day of application submission. Please refer to the Cost Guidance document provided for the standard references available.

**Personnel Costs**

This category includes salary for direct project staff roles such as researchers, scientists, engineers, and investigators. This category also covers contractors on your project team who will be working directly on the project. Please indicate if individual is a contractor. Back-office project staff may be included in this category so long as they are directly supporting the project activities (such as project managers). Otherwise, they should be included under Indirect (Overhead) Costs. 

**Total Cost of Employment** typically includes gross salary, National Insurance, company pension contribution, life insurance or other non-discretionary package costs, or equivalent employer taxes and social security contributions for non-UK applicants.

The **Number of Working Days** is calculated by taking the number of working days (total working days less holiday and bank holidays).  
If you do not know exactly who is working on the project, please estimate the salary which will be paid. Note, only actual salaries paid are able to be recovered. 

**Materials and Minor Equipment Costs**

Please include the costs of materials and/or minor equipment purchased from third parties and to be used directly / consumed during the duration of the project. If the material and/or minor equipment has a residual or resale value at the end of your project, the value should be reduced from the costs accordingly. If you are using materials and/or minor equipment supplied by collaborators, these must be listed at cost.

Only minor equipment purchases are allowed (defined as £25,000 or below per item). These may include small-scale equipment such as research supplies, minor hardware, etc. Large equipment purchases (typically above £25,000) are classified as capital expenditure and thus, not eligible.

**Licensing and Access Costs**

Only licences and access fees essential for the research activities are eligible. Costs must be proportionate to the project duration (4–6 months). Perpetual licences are not allowed unless more cost-effective than time-limited ones.

**Travel and Subsistence Costs**

Please ensure that the travel, accommodation, and meals included are necessary for project activities. Full details on spending caps and allowances are provided in the Cost Guidance. These may be used to estimate the eligible costs to include. For the level of detail, we are only expecting a total cost per line item of: 1\) Travel/Transportation, 2\) Subsistence / Meals, and/or 3\) Accommodation, as applicable to you. 

**Indirect (Overhead) Costs**

There are 2 options for claiming grant for overhead, please select one of these options: 1\) No overheads, 2\) The 20% of labour costs option. If no overheads, remove the item from the table. 

 

**Additional Information:**

Costs must be directly attributed to the project.

All costs, to be eligible, must be incurred within the grant funding period. 

DSIT have the right to request additional information at any point during the GFA.

| Budget Item | Cost | Total cost per section |
| :---- | :---- | :---- |
| Personnel Costs | — | — |
| Person 1 | 60,000 | — |
| Person 2 | 60,000 |  |
| Person 3 | 15,000 |  |
| — | — | 135,000 GBP |
| Materials and Minor Equipment Costs | — | — |
| Cloud compute (AWS) | 42,500 | — |
| API credit | 10,000 |  |
| — | — | 52,500 GBP |
| Licensing and Access Costs | — | — |
| Item 1 | N/A | — |
| — | — | — |
| Travel and Subsistence Costs | — | — |
| Travel / Transportation | 6,000 | — |
| Subsistence / Meals | N/A | — |
| Accommodation | N/A | — |
| — | — |  |
| Indirect (Overhead) Costs | — | — |
| Hosting org overhead at 10% | 21,500 GBP | — |
| — | — | 21,500 GBP |

* Payment in Advance  
  * Payments will be made after a deliverable has been achieved, approved, evidenced and claimed, subject to submission of milestone-based reporting.   
  * In exceptional circumstances, depending on need, we may consider one payment in advance of activity. This will be decided on a case-by-case basis and reflected in the Funding Agreement, but could delay signatures if additional approvals are required.   
  * If you require payment in advance, please outline why below.

## Minimum Funding

New page just added on minimum funding levels.  
For this project, we can knock it down to 6 months and only 2 researchers.

Added this in the main project page. 

## Deliverables and Outputs

This section summarises the key tangible outputs expected from your project. Please list key deliverables, describing each, its format (e.g., paper, code repository, dataset, policy brief, prototype), and expected delivery date. We expect projects will typically have milestones every 3-6 months, not all of which will be published. 

Questions marked with an asterisk (\*) are mandatory and must be answered.

**Deliverables and Outputs**  
Please list key deliverables, describing each, its format (e.g., paper, code repository, dataset, policy brief, prototype), and expected delivery date. Use the \+ icon to add additional rows.

Guidance: We suggest writing 1-2 sentences for each deliverable/milestone

NOTE: blue text is an example

| Deliverable | Description | Format | Target Completion Date |
| :---- | :---- | :---- | :---- |
| Example: D1: Preliminary research paper | Initial publication summarising early findings | Research paper | Month 3 |
| D1: Dataset release | Release of the annotated reasoning traces that cover different misalignment modes | Huggingface dataset | Month 4 |
| D2: Paper release | Paper on steering reasoning combined with prompting and SFT baselines | Research paper | Month 7 |
| D3: Paper release | Paper on reasoning control for latent reasoning models, and monitoring methodology for them | Research paper | Month 12 |

## Work Plan and Timeline

This section provides a clear timeline of key activities, milestones, and success criteria for your project. For longer projects, we understand that granular planning may be inappropriate, especially for the later stages of the project. 

Questions marked with an asterisk (\*) are mandatory and must be answered.

Guidance: 1-2 sentences for each milestone

**Work Plan and Timeline**  
Provide a clear timeline of key activities, milestones, and success criteria for your project. Use the \+ icon to add additional rows.

NOTE: blue text is an example

| Month/Week | Key Activities | Milestones | Performance Metrics / Success Criteria |
| :---- | :---- | :---- | :---- |
| Example: Week 1-2 | Data collection and initial literature review | Completion of baseline research plan | Data sources identified: literature review summary completed |
| Month 1 | \- Literature review \- Dataset creation \- Infra buildout \- Start on prompting baselines | Completion of literature review for advancements up to project start date (from time of application) | Datasets identified, lit. review complete, infra buildout started |
| Month 2 | \- Finish dataset creation for CoT  \- Finish infra buildout \- Finish prompting baselines \- Work on initial steering vector extraction | Dataset finished, good infrastructure, prompting baselines showing some effect | Milestones completed, prompting baselines increasing CoT faithfulness on some prompts  |
| Month 3 | \- Begin work on SFT baselines \- Start to steer small, open weight reasoning models, compare against baselines | Review of current baseline methods and smaller steering attempts on CoT faithfulness benchmarks | Milestones completed, show performance (at this stage, okay to have baselines outperforming steering) |
| Month 4 | \- Finish work on SFT baselines \- More thoroughly test contrastive pairs steering methods \- Begin testing optimization based steering methods \- Prepare dataset for public release \- Begin initial write up of results | Baseline comparisons completed, dataset released onto HuggingFace | Performance gain on CoT monitoring, initial experiments on better steering methods **Deliverable 1**: Dataset of tagged reasoning traces |
| Month 5-6 | \- Iterate on steering methods \- Start to work on adding non-CoT faithfulness misalignment scenarios to our steering work \- Continue writing, incrementally add experiments to the work | Preliminary draft of the paper, adding to the dataset for non-CoT faithfulness scenarios | Milestones completed, new steering scenarios added if possible or thorough documentation of failure scenarios if not |
| Month 7 | \- Finish writing the paper for public release \- Last minute experiments for first paper | Release the paper, preprint on the arXiv, conference submission | **Deliverable 2:** Paper release |
| Month 8-9 | \- Start preliminary investigations on latent reasoning models \- Literature review of latent reasoning research up to current date \- New scoring metrics for latent models as current monitorability metrics will not work (no visible CoT) | Literature review completed, understanding of up to date safety metrics for latent monitoring | Milestones completed, action plan for remaining grant period |
| Months 10-11 | \- Finish developing evaluation methods for latent reasoning, with a baseline of simply tokenizing the latent stream and monitoring it \- Iterate on latent reasoning steering methods \- Begin writing of results for a preliminary paper (workshop or full conference paper) | Initial results complete for safer model outputs, basic understanding of latent reasoning | Milestones completed |
| Month 12 | \- Finish iterating on latent reasoning steering \- Finish writing paper documenting results | Release of paper, arXiv preprint and either conference or workshop submission | **Deliverable 3:** Paper release |

## Key Project Risks and Mitigation Strategies

This section briefly identifies major project risks (e.g. risks of failure to make progress) and for you to describe your mitigation strategies.

Questions marked with an asterisk (\*) are mandatory and must be answered. 

**Key Project Risks and Mitigation Strategies**  
Provide detail on any major project risks (e.g. risks of failure to make progress) and describe your mitigation strategies in the table provided. Use the \+ icon to add additional rows. 

NOTE: blue text is an example

| Risk | Likelihood (Low/Med/High) | Impact (Low/Med/High) | Mitigation Plan |
| :---- | :---- | :---- | :---- |
| Example: Delay in data access | Medium | High | Establish agreements early, identify alternative sources |
| Delay in access to proper compute | Low | Medium | Establish early on which compute providers, stay in close contact with AISI to get appropriate funding early on |
| Concurrent research may be similar | Medium | Medium | Quickly contact other authors and groups, work on a potential collaboration so that we do not duplicate work |
| Difficult to plan more than 8 months in advance | Medium | Medium | The field moves very quickly so research we plan for the later part of the grant period is more speculative, we plan to conduct thorough literature review, be in contact with other authors, and be ready to quickly adopt new approaches or pivot |

