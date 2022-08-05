This repository has been designed for use in gem5 tutorials.
It has been built with the assumption users will utilize [Codespaces](https://github.com/features/codespaces) to learn gem5.

The repository contains the following directories:

* [docker](docker) :
The source code for the Docker image used by [.devcontainer/Dockerfile](.devcontainer/Dockerfile) to create the Codespace Docker container.
* gem5 :
v22.0.0.1 of gem5.
* gem5-resources :
gem5-resources which may be used with v22.0 of gem5.
* materials: Example materials used as part of the tutorial.
* modules: Source for the accompying website: https://gem5bootcamp.github.io/gem5-bootcamp-env
The website contains links to slides, presentation videos, and notes for the tutorials.

**Note:** 'gem5' and 'gem5-resources' are submodules though the [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json) file specifies that a `git module update --init --recursive` command is executed when the Codespace Docker container is created.

The container used by Codespaces is built from [.devcontainer/Dockerfile](.devcontainer/Dockerfile).
It contains:

* All gem5 dependencies (inc. optional dependencies).
* Prebuilt gem5 binaries:
    - `/usr/local/bin/gem5-x86`
    - `/usr/local/bin/gem5-arm`
    - `/usr/local/bin/gem5-riscv`
* A RISCV64 and an AARCH64 GNU cross-compiler:
    * RISCV64 GNU cross-compiler found in `/opt/cross-compiler/riscv64-linux/`.
    * AARCH64 GNU cross-compiler found in `/opt/cross-compiler/aarch64-linux/`.

## Beginners' example

The following can be used within the Codespace container to run a basic gem5 simulation straight away:

```
gem5-arm gem5/configs/example/gem5_library/arm-hello.py
```

This will execute a "Hello world!" program inside a simulated ARM system.

## Updating submodules

In this project we have two submodules: 'gem5' and 'gem5-resources'.
These are automatically obtained when the codespaces is initialized.
At the time of writing the 'gem5' directory is checked out to the stable branch at v22.0.0.1.
The 'gem5-resources' repository is checkoued out to revision '871e715', which should contain resources with known compatibility with gem5 v22.0.

To update the git submodules to be in-sync with their remote origins (that hosted on our [googlesource](https://gem5.googlesource.com)), execute the following command:

```sh
git submodule update --remote
```

This repository may be updated to these in-sync submodules by running the following (this assumes you have correct permissions to do so):

```sh
git add gem5 gem5-resources
git commit -m "git submodules updated"
git push
```

## Best practises

### Using branches

A good strategy when working with gem5 is to use branches.
In the 'gem5' directory, you can use branches to segregate your development.
A typical workflow would be as follows.

1. Start from the stable branch.
This will ensure you are starting from a clean, stable version of gem5.

```sh
git checkout stable
```

2. Create another branch to work on.
Initially this branch will be idential to stable but with a name of your choosing.

```sh
git branch example-1 # Creating a new branch named 'example-1'.
```

3. Checkout this branch:

```sh
git checkout example-`
```

4. Make changes on this branch and commit the changes.
For example:

```sh
echo "Create a test commit" >test.txt
git add test.txt
git commit -m "misc: Adding a test commit"
```

5. When done, or wishing to move onto something else, checkout stable.
This effectively reverts the changes made on the branch.

```sh
git checkout stable
```

6. You may return to this branch whenever you want.

```sh
git checkout example-1
```

To see a list of all available branches you can execute:

```sh
git branch
```
