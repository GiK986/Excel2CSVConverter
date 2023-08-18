@echo off
call .\venv\Scripts\activate
call python .\converter.py
call .\venv\Scripts\deactivate
