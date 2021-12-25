# TAL-PoC
* There are several objectives to achieve the PoC.
  * Log-in/Log-out to Kiwoom
  * Inquiry about asset status
  * Buy/Sell individual a stock
  * Buy/Sell individual stocks
  * Rebalancing investstments


>git comment one time used by ethan when setup dev environment in new PC
>>git config --list<br>
>>git config --global user.name “Your Name”<br>
>>git config --global user. email “name@email.com”<br>

>repository rule setup. (It is required to block merging code to 'main' branch directly by someone including admin) 
>>1) Settings - Manage access - add a collaborator, 'dr-robo'. After that he/she has to accept my invitation.
>>2) Settings - Branches - 'main' branch is my root  branch. So add the 'main' branch in 'Branch protection rules' with the options properly for us to be used.
>>3) create a branch clonned from the 'main' branch.
>>4) Clone a Specific Branch : git clone -b <branchname> <remote-repo-url>
