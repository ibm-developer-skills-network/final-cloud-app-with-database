# Please, READ and Delete this section before publishing your lab

Welcome to your Theia-based Course Labs.  

Let's move on with building your lab. This file you are in (coding-labs.md) is the place where you create the the instructions for your course users to follow. Here are a few recomendations:
* divide your labs in to steps with each step having a goal your lab users will achieve. You create a step by making it an `<H1>` in HTML or single hash mark `#` in markdown.
* make sure your instructions are actually teaching the concepts and not turning your users in to robots that repeat your keystrokes. This means you should be explaining the goal and what you are trying to do not just commands to get it done.
* use pictures (and videos) to illustrate your point. Put your pictures in to the `images` folder of your GitLab project. Refference your pictures in the `images` folder. Don't worry, our CI/CD process will fix the urls automatically.
* always provide a call to action at the end of the lab. Tell people about a service they should try on the IBM Cloud and give them a url for this service. Don't worry about campaign codes etc. Our CI/CD process will add proper campaign codes so that your lab will get full credit automatically.
* these are coding labs. Please use code markdown to illustrate the output and, more important, the code that .
 
### How to properly markdown code blocks

When building a Theia-based Course Lab you will find that you need to use code markdown in the following situations:
1. to display the output the user will see
2. for commands they will type in to a terminal window
3. for contents they will type in to editor while editing files that contain code

The best way to markdown output is to simply include it in a code block markdown like so:
```
some output
```

For terminal commands a single code line marked down as \`ls\`{: codeblock} would render as `ls` is typically the best option. The `{: codeblock}` keyword right after your sigle line code markdown will put a handy copy-to-clipboard button next to your code. Your users will appreciate it.

For content that you expect people to type in to an editor, a multi-line code block markdown is the best option. Use triple back ticks to indicate multi-line code blocks:
```
let name = "Skills Network";
console.log(name);
```

To make it easier for users to copy and paste code, both single line and multi-line code block, append append the key {: codeblock} at the next line, immediately after the end of the code block. For example:

```
let name = "Skills Network";
console.log(name);
```
{: codeblock}

This displays a copy to clipboard button for your readers and allows them to copy your code with a single click. No more highlighting the text, clicking on `Ctrl+C` (`Command+C` on Apple Mac) and possibly missing a few characters.

Please note that there are some limitations in the markdown we can process so it is best to stay clear of these:

* We currently cannot hyper-link to a specific step on the Theia-based Course Labs
* Don't indent code blocks and images
* Don't nest numbered lists as it causes unexpected behaviors.


**We do recommend that you use the following as an outline for your lab**

---
Please, remember to delete everything above before publishing your lab.

---


# Title
Make the title short and meaningfull. Let the title give people an idea of what to expect not the steps. 

This is the section where you want to welcome people to your lab and to excite them with an expectation of what they will be able to learn. Please don't be dry and boring; that is what bad university lectures are for. People spend time on your lab not because they have to but because they want to. Please, make it worth their while. 

## Learning Objectives
Tell your audience what they can expect to learn. Better yet, tell them what they will be able to do as a result of completing your lab.

## Prerequisites (optional)
List the prior knowledge if any, required to take this tutorial

# Step 1: learn something simple
This is the first section. You may have as many sections as you want

# Step 2: advance to the next step
Now we are rolling. 

...

# Step n: another step in conquering knowledge
You may have as many sections as you want

# Summary
Summarize key learning points against the learning objectives. Make the user feel good about what they have achieved. Also, tell tehm if they did miss something they can always come back and do the lab agian.

# Next Steps
Tell people what they should explore next. Here is an example:

In this lab you got to deploy your Node.js application to a Kubernetes cluster. You used a shared cluster provided to you by the IBM Developer Skills Network. If you are interested in continuing to learn about Kubernetes and containers, you should get your own [free Kubernetes cluster](https://www.ibm.com/cloud/container-service/) and your own free [IBM Container Registry](https://www.ibm.com/cloud/container-registry).
