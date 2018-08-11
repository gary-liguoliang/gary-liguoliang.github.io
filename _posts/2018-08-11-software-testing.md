---
layout: post
title:  "'Software Testing Foundations' Notes"
date:  2018-08-11 23:00:00 +0800
categories: qa
tags:
 - qa
---

*randomly copied from: [Software Testing Foundations, 4th Edition](https://www.amazon.com/Software-Testing-Foundations-4th-Certified/dp/1937538427)*

## The Fundamental Test Process

### Test Planing and Control
Planning of the test process starts at the beginning of the software development project.
The mission and objectives of testing must be defined and agreeed upon as well as the resources necessary for the test process.

The main task of planning is to determine the `test strategy` or approach. since an exhaustive test is not possible, 
priorities must be set based on risk assessment. The test activities must be distributed to the individual subsystems, 
denpending on the expected risk and the sverity of failure effects. 

### Test Analysis and Design
The first task is to review the test basis, i.e., the specification of what should be tested. the specification should be 
concrete and clear enough to develop test cases. the basis for the creation of a test can be the specification or architecure documents.

it is important to ensure `traceability` between the specifications to be tested and the tests themselves. 
it must be clear which test cases test which requirement and vice versa. Only this way is it possible to decide which requirements
are to be or have been tested, how intensively and with which test cases.Even the traceability of requirement changes to the test cases
and vice versa should be verified. 

### Test Implementation and Execution
Tests must be run and logged.
the priority of the test cases decided during planning. 

### Test Evaluation and Reporting
During test evaluation and reporting, the test object is assessed against the set test exit criteria specified during planning. 
this ma result in normal termination of the tests if all criteria are met, or it may be decided that additional test cases 
should be run or that the criteria weree too hard. 
it must be decided whether the test exit criteria defined in the test plan are fulfilled.

### Test Closure Activities
the following data should be recorded:
 - when wwas the software system released?
 - when was the test finished or terminated? 
 - when was a milestone reached or a maintenane release completed?
 Importeant informantion for evaluation can be extracted by asking the following questions:
  - which planned results are achieved and when -- if at all?
  - which unexpected events happened (reasons and how they were met)?
  - are there any open problems? and change requests? why ere thye not implemented? 
  - how was user acceptance after deploying the system?
  
  
## General Principles of Testing
 - Testing shows the presence of defects, not their absence. Testing can show that the product fails, cannot prove that a program is defect free.
  even if no failures are found during testing, this is no proof that there are no defects. 
 - Exhaustive tesing is impossible
   it's impossible to run an exhaustive test that includes all possible values.
 - Testing activities should start as early as possible
 - Defect clustering. if many defects are detected in one place, there are normally more defects nearby. 
 - The [pesticide paradox](https://sqa.stackexchange.com/questions/6440/what-is-meant-by-the-term-pesticide-paradox-in-testing-point-of-view). new and modified cases should be developed and added to the test. 
 - Testing is context dependent.
 - No failures means the system is useful is a fallacy.
 
 
## Test Plan
 The test manager might participate in the following planning activities:
  - defininingthe overall approach to and strategy for testing
  - deciding about the test environment and test auotomation
  - defining the test level and their interaction and integrating the testing activities with other project activities
  - deciding how to evaluate the test results
  - selecting matrics for monitoring and controlling test work, as well as defining test exit criteria
  - determining how much test documentation shall be prepared and determining templates
  - writing the test plan and deciding on what, who, when and how much testing
  - estimating test effor and test cost.
    
### Test Entry and Exit Criteria
  *typial entry criteria:*
   - the test environment is ready
   - the test tools are ready for use in the test environment
   - test objects are installed in the test environment
   - the necessary test data is available
   
  *exit:*
   - achieved test coverage: tests run, covered requirements, code coverage etc.
   - product quality: defect density, defect severity, failure rate and reliability of the test object
   - residual risk: tests not executed, defects not repaired, incomplete coverage of requirements or code. ect.
   - economic constraints: allowed cost, project risks, release deadlines and market chance. 
  
**Test Plan according to IEEE 829-1998**
- Test Plan Identifier
- Introduction
- Test Items
- Features to be Tested
- Features not to be Tested
- Approach
- Item Pass/Fail Criteria (exit criteria)
- Suspension Criteria and Resumption Requirements
- Test Deliverables
- Testing Tasks
- Environmental Needs
- Staffing and Training Needs
- Schedule
- Risks and Contingencies
- Approvals




 
