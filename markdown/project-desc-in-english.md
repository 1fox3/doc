## 1-minute version

Good morning everyone. Today I’d like to give a quick introduction to GRCA, which stands for Generic RCA. GRCA is a self-service platform that helps users design, manage, and execute root cause analysis pipelines in a more efficient and scalable way.

The main goal of GRCA is to reduce manual investigation effort. Instead of checking multiple systems separately, users can configure an analysis pipeline, run a job, and review the results in a structured way.

In GRCA, the core concepts are use case, pipeline, and job. A use case groups pipelines for a certain business area. A pipeline is built as a DAG of nodes, and a job is one execution of that pipeline with specific input parameters.

Another important benefit is flexibility. GRCA can integrate with Bennu for data access, and it can also work with different analysis capabilities such as algorithms, LLMs, and code-based logic to support different RCA scenarios.

In short, GRCA helps teams make RCA work more automated, reusable, and standardized.


## 3-minute version

Good morning everyone. Today I’d like to introduce GRCA, or Generic RCA. GRCA is a self-service RCA platform that enables users to design, manage, and execute root cause analysis pipelines with better efficiency, visibility, and scalability.

The reason GRCA is important is that root cause analysis is often a very manual process. In many cases, engineers or analysts need to check dashboards, query data from different systems, compare results, and then summarize the possible reasons behind an issue. GRCA is designed to simplify that process by turning investigation logic into configurable pipelines, so the analysis can be executed in a more automated and repeatable way.

There are three basic concepts in GRCA: use case, pipeline, and job. A use case is a collection of pipelines for one business domain or scenario. A pipeline is the actual analysis workflow, built as a tree-like node structure that represents a DAG of processing units. A job is a single execution of a pipeline with a set of input parameters. After the job is triggered, users can review the detailed output of each node on the result page.

GRCA is also flexible in terms of technical integration. For example, it can connect with Bennu to fetch data, and it can orchestrate different analysis capabilities in one pipeline. These capabilities may include anomaly detection algorithms, LLM-based analysis, and code-based processing. Because of this, GRCA can support a wide range of RCA scenarios instead of only one fixed workflow.

From a business and engineering perspective, one of the biggest values of GRCA is standardization. By registering pipelines and following RCA SOPs, teams can reuse the same investigation logic across similar cases, reduce duplicated manual work, and improve analysis consistency.

So, in summary, GRCA is not just a tool for running analysis. It is a configurable RCA framework that helps teams build automated, reusable, and scalable investigation workflows. That is why it can improve both efficiency and analysis quality in day-to-day RCA work.

Thank you.
