#!/usr/bin/env bash

# This script compiles all $PROGRAMS_FOLDER programs to mir
PROGRAMS_FOLDER="programs"
COMPILED_PROGRAMS_FOLDER="programs-compiled"

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}" 2>/dev/null)" && pwd -P)"
TARGET_PATH="${SCRIPT_PATH}/${COMPILED_PROGRAMS_FOLDER}"
PROGRAMS_PATH="${SCRIPT_PATH}/${PROGRAMS_FOLDER}"

PYNADAC="pynadac"

cd "${PROGRAMS_PATH}" || exit 1

for file in *.py ; do
  echo "Compiling ${file}"
  "$PYNADAC" --target-dir "${TARGET_PATH}" \
    --generate-mir-json \
    "${file}"
done 

echo "------------------------"
echo "Compiled programs: all files in the programs directory were compiled to mir: [$TARGET_PATH]"

echo "Now try running an example:"

echo "----------single party compute --------------"

echo "Code for single party compute lives in the examples_and_tutorials/core_concept_client_single_party_compute folder"
echo "📋 to run single party compute - addition_simple program: 'cd examples_and_tutorials/core_concept_client_single_party_compute && python3 addition_simple.py'"

echo "----------multi party compute --------------"

echo "Code for multi party compute lives in the examples_and_tutorials/core_concept_multi_party_compute folder"
echo "📋 to run multi party compute in 3 steps - addition_simple_multi_party_3: 'cd examples_and_tutorials/core_concept_multi_party_compute && python3 01_store_secret_party1.py'"