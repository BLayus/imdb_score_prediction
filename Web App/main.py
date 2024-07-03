{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "2d0d2072",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: streamlit in d:\\8_software\\anaconda\\lib\\site-packages (1.36.0)\n",
      "Requirement already satisfied: pydeck<1,>=0.8.0b4 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (0.9.1)\n",
      "Requirement already satisfied: protobuf<6,>=3.20 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (5.27.2)\n",
      "Requirement already satisfied: requests<3,>=2.27 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (2.32.3)\n",
      "Requirement already satisfied: altair<6,>=4.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (5.3.0)\n",
      "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (3.1.43)\n",
      "Requirement already satisfied: watchdog<5,>=2.1.5 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (4.0.1)\n",
      "Requirement already satisfied: pillow<11,>=7.1.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (8.2.0)\n",
      "Requirement already satisfied: toml<2,>=0.10.1 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (0.10.2)\n",
      "Requirement already satisfied: typing-extensions<5,>=4.3.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (4.12.2)\n",
      "Requirement already satisfied: tornado<7,>=6.0.3 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (6.1)\n",
      "Requirement already satisfied: click<9,>=7.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (7.1.2)\n",
      "Requirement already satisfied: pandas<3,>=1.3.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (2.0.3)\n",
      "Requirement already satisfied: numpy<3,>=1.20 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (1.24.4)\n",
      "Requirement already satisfied: cachetools<6,>=4.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (5.3.3)\n",
      "Requirement already satisfied: packaging<25,>=20 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (20.9)\n",
      "Requirement already satisfied: rich<14,>=10.14.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (13.7.1)\n",
      "Requirement already satisfied: pyarrow>=7.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (16.1.0)\n",
      "Requirement already satisfied: tenacity<9,>=8.1.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (8.4.2)\n",
      "Requirement already satisfied: blinker<2,>=1.0.0 in d:\\8_software\\anaconda\\lib\\site-packages (from streamlit) (1.8.2)\n",
      "Requirement already satisfied: jinja2 in d:\\8_software\\anaconda\\lib\\site-packages (from altair<6,>=4.0->streamlit) (2.11.3)\n",
      "Requirement already satisfied: toolz in d:\\8_software\\anaconda\\lib\\site-packages (from altair<6,>=4.0->streamlit) (0.11.1)\n",
      "Requirement already satisfied: jsonschema>=3.0 in d:\\8_software\\anaconda\\lib\\site-packages (from altair<6,>=4.0->streamlit) (3.2.0)\n",
      "Requirement already satisfied: gitdb<5,>=4.0.1 in d:\\8_software\\anaconda\\lib\\site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.11)\n",
      "Requirement already satisfied: smmap<6,>=3.0.1 in d:\\8_software\\anaconda\\lib\\site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.1)\n",
      "Requirement already satisfied: setuptools in d:\\8_software\\anaconda\\lib\\site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (52.0.0.post20210125)\n",
      "Requirement already satisfied: pyrsistent>=0.14.0 in d:\\8_software\\anaconda\\lib\\site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.17.3)\n",
      "Requirement already satisfied: attrs>=17.4.0 in d:\\8_software\\anaconda\\lib\\site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (20.3.0)\n",
      "Requirement already satisfied: six>=1.11.0 in d:\\8_software\\anaconda\\lib\\site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (1.15.0)\n",
      "Requirement already satisfied: pyparsing>=2.0.2 in d:\\8_software\\anaconda\\lib\\site-packages (from packaging<25,>=20->streamlit) (2.4.7)\n",
      "Requirement already satisfied: pytz>=2020.1 in d:\\8_software\\anaconda\\lib\\site-packages (from pandas<3,>=1.3.0->streamlit) (2021.1)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in d:\\8_software\\anaconda\\lib\\site-packages (from pandas<3,>=1.3.0->streamlit) (2.9.0.post0)\n",
      "Requirement already satisfied: tzdata>=2022.1 in d:\\8_software\\anaconda\\lib\\site-packages (from pandas<3,>=1.3.0->streamlit) (2024.1)\n",
      "Requirement already satisfied: MarkupSafe>=0.23 in d:\\8_software\\anaconda\\lib\\site-packages (from jinja2->altair<6,>=4.0->streamlit) (1.1.1)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in d:\\8_software\\anaconda\\lib\\site-packages (from requests<3,>=2.27->streamlit) (2020.12.5)\n",
      "Requirement already satisfied: idna<4,>=2.5 in d:\\8_software\\anaconda\\lib\\site-packages (from requests<3,>=2.27->streamlit) (2.10)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in d:\\8_software\\anaconda\\lib\\site-packages (from requests<3,>=2.27->streamlit) (1.26.4)\n",
      "Requirement already satisfied: charset-normalizer<4,>=2 in d:\\8_software\\anaconda\\lib\\site-packages (from requests<3,>=2.27->streamlit) (3.3.2)\n",
      "Requirement already satisfied: markdown-it-py>=2.2.0 in d:\\8_software\\anaconda\\lib\\site-packages (from rich<14,>=10.14.0->streamlit) (3.0.0)\n",
      "Requirement already satisfied: pygments<3.0.0,>=2.13.0 in d:\\8_software\\anaconda\\lib\\site-packages (from rich<14,>=10.14.0->streamlit) (2.18.0)\n",
      "Requirement already satisfied: mdurl~=0.1 in d:\\8_software\\anaconda\\lib\\site-packages (from markdown-it-py>=2.2.0->rich<14,>=10.14.0->streamlit) (0.1.2)\n"
     ]
    }
   ],
   "source": [
    "!pip install streamlit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "6956c7c0",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "705fbdcd",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "UsageError: Line magic function `%` not found.\n"
     ]
    }
   ],
   "source": [
    "% streamlit run streamlit_app.py"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "45a36501",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
