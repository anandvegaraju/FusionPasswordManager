# FusionPasswordManager
A convenient and simple tool that allows you to update passwords of several user accounts in one go. Works for Oracle Fusion Cloud applications.

# Steps

1.  Download the executable from here -> https://drive.google.com/file/d/1FcG8SbdSgXWiszP3QXv37bDKF3Dek79b/view?usp=sharing
2.  Open the exe. Enter your instance URL, Username, password.
3.  The instance URL should be of the format - https://servername.fa.us2.oraclecloud.com
4.  Ensure your user account is active and has sufficient privileges to use REST services (User account) and IT Security Manager role assigned.
4.  Click on the Run button and select your xls/xlsx file containing 2 columns (Username, Password).
5.  Wait for the application to process the file, update the passwords and display the response.



# Steps to ensure you have the right roles and privileges

From Navigator->Tools->Security Console->search for the seeded Human Capital Management or HCM Integration Specialist Job Role and

a. click Copy under the drop-down LOV, and select Copy top role and inherited Roles
b. give the role a unique custom name
c. under the Functional Security Policies section or stop, ensure that the 'Use REST Service - User Accounts' policy is present. If it's not there, please click on Add Functional Security Policy button to add the policy
d. under the Users section or stop, remove the the REST API user, if present
e. under the Summary section or stop, please click Save and Close

--View All Data Role Setup--

1. Navigate to Setup and Maintenance work area, search for and select the "Manage Data Role and Security Profiles" task. The Manage Data Role and Security Profiles page opens.
2 Click Create to create a new data role ,and include a name is such as "View_All_HCM_Integration_Specialist". In the job role Click in drop down, Select Search and search for your custom HCM Integration Specialist Job Role.
4. Click Next. Select "View All " for each area

a. Organization Security Profile = View All Organizations
b. Position Security Profile = View All Positions
c. Country Security Profile = View All Countries
d. Person Security Profile =View All People
e. Public Security Profile=View All People
f. Click Next.......until reaching Review ...Click Submit

5. Assign data role to your REST API user

a. Navigate to Tools->Security Console
b. Click on Users icon / tab
c. Search and edit the user which has the custom or seeded HCM Integration Specialist Role
d. Click Add Role
e. Search and add the “View_All_HCM_Integration_Specialist"
f. Click Done, then Save and Close

If you already have a custom HCM Integration Specialist--with an associated View All Data Role assigned to your user--then

1. Edit your custom HCM Integration Specialist User by adding the 'Use REST Service - User Accounts' Functional Security Policy
2. From the Setup & Maintenance 'Manage Data Role and Security Profiles' Task, search for the existing custom View All Data Role Job
3. Select the View All Data Role associated with your custom or seeded HCM Integration Specialist Job Role and Click Edit
4. Next, ensure that "View All" is selected for each area

a. Organization Security Profile = View All Organizations
b. Position Security Profile = View All Positions
c. Country Security Profile = View All Countries
d. Person Security Profile =View All People
e. Public Security Profile=View All People
f. Click Next.......until reaching Review ...Click Submit

5. click on Run User and Roles Synchronization Process task from Setup & Maintenance,
6. Confirm status of ESS Job via Navigator->Tools->Scheduled Processes, and click refresh. If this process hasn't run for some time, it may takes hours--maybe longer--to complete.
7. Also run Send Pending LDAP ESS Job
