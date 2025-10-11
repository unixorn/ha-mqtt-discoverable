<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Description](#description)
- [Credit](#credit)
- [License Acceptance](#license-acceptance)
- [Developer Certificate of Origin (DCO)](#developer-certificate-of-origin-dco)
- [Type of changes](#type-of-changes)
- [Checklist](#checklist)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<!-- Provide a general summary of your changes in the Title above -->

# Description

<!-- Describe your changes in detail -->

# Credit
<!-- Releases are announced on Mastodon. In order for me to credit people properly, -->
<!-- if you have a mastodon account, please put it here to have it mentioned in the -->
<!-- release announcement. If there's another way you want to be credited, please   -->
<!-- add details here. -->

# License Acceptance

- [ ] This repository is Apache version 2.0 licensed and by making this PR, I am contributing my changes to the repository under the terms of the Apache 2 license.

# Developer Certificate of Origin (DCO)

The Developer Certificate of Origin (DCO) is a lightweight way for contributors to certify that they wrote or otherwise have the right to submit the code they are contributing to the project. Here is the full text of the DCO, reformatted for readability:

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I have
    the right to submit it under the open source license indicated in the
    file; or

    (b) The contribution is based upon previous work that, to the best of
     my knowledge, is covered under an appropriate open source license and
     I have the right under that license to submit that work with
     modifications, whether created in whole or in part by me, under the
     same open source license (unless I am permitted to submit under a
     different license), as indicated in the file; or

    (c) The contribution was provided directly to me by some other person
    who certified (a), (b) or (c) and I have not modified it.

    (d) I understand and agree that this project and the contribution are
    public and that a record of the contribution (including all personal
    information I submit with it, including my sign-off) is maintained
    indefinitely and may be redistributed consistent with this project or
    the open source license(s) involved.

Contributors sign-off that they adhere to these requirements by adding a `Signed-off-by` line to commit messages.

```
This is my commit message

Signed-off-by: Random J Developer <random@developer.example.org>
```

Git even has a `-s` command line option to append this automatically to your commit message:

```sh
git commit -s -m 'This is my commit message'
```

# Type of changes

<!-- What types of changes does your submission introduce? Put an `x` in all the boxes that apply: [x] -->

- [ ] Add/update a helper script
- [ ] Add/update link to an external resource like a blog post or video
- [ ] Bug fix
- [ ] New feature
- [ ] Test updates
- [ ] Text cleanups/updates
- [ ] New release to PyPi
- [ ] Documentation update

# Checklist

<!-- Go over all the following points, and put an `x` in all the boxes that apply. [x] -->
<!-- If you're unsure about any of these, don't hesitate to ask. I'm happy to help! -->

- [ ] I have read the [CONTRIBUTING](https://github.com/unixorn/ha-mqtt-discovery/blob/main/Contributing.md) document.
- [ ] I have signed off my commits per the DCO
- [ ] All new and existing tests pass.
- [ ] Any scripts added use `#!/usr/bin/env interpreter` instead of potentially platform-specific direct paths (`#!/bin/sh` is an allowed exception)
- [ ] Scripts added/updated in this PR are all marked executable.
- [ ] Scripts added/updated in this PR _do not_ have a language file extension unless they are meant to be sourced and not run standalone. No one should have to know if a script was written in bash, python, ruby or whatever. Not including file extensions makes it easier to rewrite the script in another language later without having to change every reference to the previous version.
- [ ] I have confirmed that any links added or updated in my PR are valid.
