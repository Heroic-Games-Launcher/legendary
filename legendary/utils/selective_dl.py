# This file contains utilities for selective downloads in regards to parsing and evaluating sdlmeta
# coding: utf-8

import os
import json
from epic_expreval import Tokenizer, EvaluationContext

def has_access(context, app):
    return bool(context.core.get_game(app))

def is_selected(context, input):
    return input in context.selection

EXTRA_FUNCTIONS = {'HasAccess': has_access, "IsComponentSelected": is_selected}

class LGDEvaluationContext(EvaluationContext):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.selection = set()

    def reset(self):
        super().reset()
        self.selection = set()

def run_expression(expression, input):
    """Runs expression with default EvauluationContext"""
    tk = Tokenizer(expression, EvaluationContext())
    tk.compile()
    return tk.execute(input)

def get_sdl_data(location, app_name, app_version):
    applying_meta = []
    for sdmeta_file in location.glob('*sdmeta'):
        sdmeta = json.loads(sdmeta_file.read_text('utf-8-sig'))
        is_applying_build = any(
            build
            for build in sdmeta.get('Builds')
            if build.get('Asset') == app_name
            and run_expression(build['Version'], app_version)
        )
        if is_applying_build:
            applying_meta.append(sdmeta)
            
    if applying_meta:
        return applying_meta[-1]
    return None
