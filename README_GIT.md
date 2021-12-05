# General Workflow in Git
After [adding an ssh key to your computer](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) you can download the git repository to your computer with the following command:

`git clone git@github.com:lennardkorte/CTC-Project.git`

Note: avoid using the https links given. You'd have to repeadedly log in with that, which can be really annoying.

### Always before you make any changes, make sure you check that:
1. Every group has its own branch on which they can work on. There are three branches right now: master-ImageImpainting, master-ObjectDetection, master-Server
    Only make changes to the branch of your group or one created by yourself.
    Check that you are working on the right branch: `git branch -a`
    -> if not change it with: `git checkout <branchName>`
2. Check that the branch you are working on is up to date. Otherwise you will have problems with your commit later: `git pull`

### Always after making changes to your branch:
1. Check that your programm compiles without errors and all the things that worked before still work. Otherwise others can't continue working on it.
2. If the changes work well add all files and subdirectories to create a commit: `git add .` Then commit your changes with: `git commit -m "<commitMessage>"`
3. If you want to synchronise your changes with GitHub and make them available to the group, type: `git push`

### Always after introducing major changes and introducing new functionality to your branch
Changes from a groups branch can be included into the main branch, if major changes have been done and new functionalities have been added:
1. Visite your modified branch and the main branch with `git checkout <branchName>` and update each with `git pull`
2. Go back to your modified branch and merge updates of the main branch into yours first: `git merge main` Only then you can merge the changes of your own modified bracnh into the main bracnh later. Confricts may arise. Solve them if needed. Then add and commit the changes as specified above.
3. Set up a new [merge/pull request](https://github.com/lennardkorte/CTC-Project/pulls) on the website. (main <- modifiedBranch) Someone else can then check and approve them. Everything should then be merged into the main branch without any errors.
