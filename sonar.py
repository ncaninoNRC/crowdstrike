from sonarqube import SonarCloudClient

url = 'https://sonarcloud.io'
cloudToken = 'ed67483859ec558a6f950ad7a096ba5b26cf5bcd'
sonar = SonarCloudClient(sonarcloud_url=url, token=cloudToken)
org = 'nationalresearchcorporation'

# issues1 = list(sonar.issues.search_issues(statuses=open))

#issues2 = list(sonar.issues.search_issues(componentKeys=org, statuses="OPEN"))

# issues3 = list(sonar.issues.search_issues(projects="blackbird", statuses="OPEN"))

# print(issues3)




sonarProjects = list(sonar.projects.search_projects(organization=org, projects="airflow-pipeline2"))

print(sonarProjects)


##### works
# accounts = sonar.issues.search_scm_accounts(org)

# print(accounts)