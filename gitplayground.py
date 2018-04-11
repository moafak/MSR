import git
import pandas as pd
from io import StringIO

#Author: 		moafak.m@gmail.com
#Date:	 		2018-04-11
#Description:	display git history of a repository showing added and modified files in last n commit
#Version:		1.0.0

#outpt long strings
pd.set_option('display.max_colwidth', -1)

#open the repo
REPO_PATH = raw_input('Please enter local repository path?\n')
repo = git.Repo(REPO_PATH)
git_bin = repo.git

#limit the commit count
commits_count = 100

#git log commits
git_log = git_bin.execute('git log --all --no-merges --pretty=tformat:"%H|%aN|%ad|%s" ' + '-' + str(commits_count))

commits_in_repo = pd.read_csv(StringIO(git_log), 
    sep="|",
    header=None,              
    names=['sha', 'author', 'timestamp', 'subject']
    )

#add new column to dataframe
commits_in_repo['files_in_commit'] = ""

for (idx, row) in commits_in_repo.iterrows():
	#get files Added or Modified in the commit
	files_in_commit = git_bin.execute('git diff-tree --no-commit-id --name-status -r ' + row.loc['sha'] + ' --diff-filter=AM')
	
	#wrap each line in a div for better discard on the output
	files_in_commit = files_in_commit.replace("M\t", "<div>M&nbsp;&nbsp;")
	files_in_commit = files_in_commit.replace("A\t", "<div>A&nbsp;&nbsp;")
	files_in_commit = files_in_commit.replace("\n", "</div>")
	
	row.loc['files_in_commit'] = files_in_commit
	
	#trim the long sha for better display on the output
	row.loc['sha'] = row.loc['sha'][:7]

#re-arrange the columns of the dataframe
commits_in_repo = commits_in_repo[['sha', 'author', 'files_in_commit', 'subject', 'timestamp' ]]

#create the html output, do not escape html elements
html_output = commits_in_repo.to_html(escape=False, justify='start')

#write the html file to disk
with open('git_log.html', 'w') as fo:
    fo.write(html_output.encode('utf8'))
	
print 'end of script'	

