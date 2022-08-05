---
title: Contributing to gem5
author: Bobby Bruce
slides_code: EQLtRAKI94JKjgk5pBmJtG8B3ssv9MaR0a2i92G0TwHK8Q?e=KN3NIppm2kg
livestream_code: T67wzFd1gVY
---

In this section, we learn how to contribute to gem5

This page closely follows the slides.
Please consider these as notes for the presentation.
It may be helpful to reference the slides while following these notes.

**Important note:** This module is somewhat flawed "in the wild" as CodeSpaces does not allow users to contribute to Gerrit from the CodeSpace.
This is something that needs fixed before this is tried again.
This bug only affects people who work from the forked CodeSpace, not from the main repo.

## Our strategy

We want to teach people how to use gem5 so they use gem5.
We want people to use gem5 so they'll develop for gem5.
We want people who develop gem5 to contribute to gem5.
We want contributions to improve the project.
We want improvements to the project to garner interest.
We want this interest to result in more people learning gem5.

## Why should I contribute to gem5?

If you've:

* You've found a bug and have a fix.
* You've developed something useful and want to share it.
* Get yourself known in the project.
* It's good PR for your research to have it incorporated into gem5.
* Looks good on your CV
* Companies contribute to gem5 all the time.

## "I'm scared"

Understandable!
Very few patches get in straight away.
Most patches are only accepted after requests for changes.

We try our best to keep feedback as constructive as possible (don't take it personally!).

The purpose of this session is to make it less scary.

## Where do I make changes?

We are making changes to the gem5-website repository.

We strongly recommend users create their own branch with `git switch -c my-change`.

In this example they are working atop the gem5-stable branch.
This is permitted for the gem5-website repository.
If your patch is accepted the website will be updated with that change ASAP.

You may work atop the "develop" branch if your change to the website should be published upon the next major gem5 release (good for next release documentation updates).

## What about the other gem5 repos?

In the gem5-resources repo you can build atop "stable" to make changes for the current release.
You can build atop "develop" to make changes for the upcoming release.

## What about other gem5 repos?

### gem5 Resources

Build atop "stable" to make changes for the current release.

Built atop  "develop" to make changes for the upcoming release.

### gem5

Build atop "develop to make changes.
You cannot push to the "stable" branch.

## Making changes

### CPP

Please conform to to the [gem5 CPP style guide](https://www.gem5.org/documentation/general_docs/development/coding_style/​) (a [high-level overview is available in the gem5 repository](https://www.gem5.org/contributing#making-modifications)).

Doxygen is highly recommended when making changes to CPP code.
Doxygen is automatically generated to create: http://doxygen.gem5.org.

### Python

To format Python we utilize Python black:

```sh
pip install black
black <python file>
```

For variable/method/etc. naming conventions, please follow the [PEP 8 naming convention recommendations](https://peps.python.org/pep-0008/#naming-conventions).
While we try our best to enforce naming conventions across the gem5 project, we are aware there are instances where they are not.
In such cases please **follow the convention of the code you are modifying**.


### The biggest gotchas!

* Whitespaces at the end of a line.
* Indentation not 4 space characters (please, no tabs)
* Lines too long (for CPP, no more than 79 characters)

## Using git

```sh
git add <files to add>
```

This adds a file to the pre-commit staging area

```sh
git commit
```

This will start the commit process, but a commit message is required.

### Commit Message rules

The rules for a gem5 commit message:

1. The header must lead with tags (see [MAINTAINERS.yaml](https://gem5.googlesource.com/public/gem5/+/refs/heads/develop/MAINTAINERS.yaml) for a list of tags).
2. Headers should be clear, short descriptions of what a patch will do.
3. Headers should be no longer than 65 characters.
4. A blank line separates the header and the patch description.
5. Descriptions can span multiple paragraphs but lines should not exceed 72 characters (this is lax rule, it's acceptable to exceed this if you're quoting code or including a URL).
6. If you're implementing a Jira request, cite the Jira URL.

### View the git log

```sh
git log
```

This will show the log of all commits.
You can use this to see how gem5 git commits look.

### Pushing to git

```sh
git push origin HEAD:refs/for/stable%wip
```

`stable` is the branch you want to contribute to.

`%wip` means the patch is "Work In Progress".

However, if you do this you'll run into an error

#### Create your Gerrit account and authenticate

1. Create an account at https://gem5-review.googlesource.com.
2. Go to User Settings.
3. Select Obtain password (under HTTP Credentials).

A new tab will open explaining how authenticate your machine thus allowing contributions to Gerrit.
Follow these instructions and try pushing again.

However, even then you'll receive an error when pushing.

#### Add the correct git-hoots

```sh
f=`git rev-parse --git-dir`/hooks/commit-msg ; mkdir -p $(dirname $f) ; curl -Lo $f https://gerrit-review.googlesource.com/tools/hooks/commit-msg ; chmod +x $f

git commit --amend --no-edit
```

This is all you need to do.
It'll append the "Change-ID" to your commits.
This is how Gerrit keeps track of your changes.
Any commit with the same Change-ID is considered to be the same change.

```sh
git log
```

Will show the change with the Change-ID applied.

You should be able to push now.

## Two Types of "Review"

**This only applies to the gem5 repository contributions.**

1. Ordinary reviewer: Liberally anyone with a gem5 Gerrit account.
2. Maintainer: An exclusive club, see [MAINTAINERS.yaml](https://gem5.googlesource.com/public/gem5/+/refs/heads/develop/MAINTAINERS.yaml) for the list.

You need sign off by a reviewer and a maintainer to get a patch into gem5.

Sometimes a maintainers will give votes for both (as a reviewer and as a maintainer) but we only recommend this for stuff the maintainer has high confidence in.
Typically, we like two separate people to sign off on a patch.

## Testing

**This only applies to gem5 repository contributions.**

- The most direct are the "Presubmit" Gerrit CI tests.
These are run when a Maintainer vote occurs and they must pass before a patch is merged into the develop branch.
- The other tests run on our [Jenkins server](https://jenkins.gem5.org).
    - Our compiler tests which are ran daily.
    These ensure that gem5 compiles with all supported compilers.
    - Our nightly tests run nightly.
    These are longer tests and typically complete in 15 hours.
    - Our weekly tests run weekly (every Friday).
    These are very long tests.
    They can take 2 days to complete.

## Open ended exercise: Make your own contribution

Here we encourage users to make their own contributions to gem5.
