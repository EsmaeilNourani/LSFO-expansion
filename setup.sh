#!/bin/bash

# Name of the submodule folder
submodule_name="S1000_Transformer_NER"

# Determine the absolute path to the submodule directory
submodule_root="$PWD/$submodule_name"

# Download huggingface compatible model for Roberta bio-lm to the submodule root
wget -O "$submodule_root/RoBERTa-large-PM-M3-Voc-hf.tar.gz" https://dl.fbaipublicfiles.com/biolm/RoBERTa-large-PM-M3-Voc-hf.tar.gz
tar -xvzf "$submodule_root/RoBERTa-large-PM-M3-Voc-hf.tar.gz" -C "$submodule_root"
rm "$submodule_root/RoBERTa-large-PM-M3-Voc-hf.tar.gz"
