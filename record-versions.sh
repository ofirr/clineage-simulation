#!/bin/bash

path_installed="."

ver_hclsim=`git --git-dir ${path_installed}/.git show -s --format=%H`
ver_clineage=`git --git-dir ~/clineage/.git show -s --format=%H`
ver_estgt=`git --git-dir ${path_installed}/eSTGt/.git show -s --format=%H`
ver_treecmp=`java -jar ${path_installed}/TreeCmp/bin/treeCmp.jar | head -n 1 | awk -F' ' '{ print $3 }'`

cat > versions.core.yml << EOF
versions:
  - HCLSIM: ${ver_hclsim}
  - CLINEAGE: ${ver_clineage}
  - eSTGt: ${ver_estgt}
  - treeCmp: ${ver_treecmp}
  - TMC: ?
EOF

pip freeze > versions.dep.pip
conda list > versions.dep.conda

