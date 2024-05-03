run_pytest_in_dir() {
  local dir_name="$1"

  # Check if the directory exists
  if [ ! -d "$dir_name" ]; then
    echo "Directory does not exist: $dir_name"
    return 1
  fi

  cd "$dir_name" || return

  for file in *.py; do
    # Check if the pattern matches at least one file
    if [ -e "$file" ]; then
      echo -e "$file\n\n"
      pytest "$file" 
      echo "[DONE] $file"
    else
      echo "No Python files found in $dir_name."
      break
    fi
  done

  cd ..  # Return to the original directory
}

cp .env.sample .env && \
python3 -m pip install -r requirements.txt && \
bash ./create_venv.sh && \
./bootstrap-local-environment.sh && \
echo "Waiting 60 seconds for preprocessing elements" && sleep 60 && \
sh compile_programs.sh && \

run_pytest_in_dir client_single_party_compute && \
cd examples_and_tutorials && \
run_pytest_in_dir core_concept_multi_party_compute && \
run_pytest_in_dir core_concept_permissions && \
run_pytest_in_dir core_concept_single_party_compute && \
run_pytest_in_dir core_concept_permissions && \
run_pytest_in_dir core_concept_store_and_retrieve_secrets && \
run_pytest_in_dir millionaires_problem_example
