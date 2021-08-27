# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_custom_dependencies]
import subprocess

from flask import make_response


def http_handler(request):
    try:
        image = __create_diagram(request.args.get('dot'))
        response = make_response(image)
        response.headers.set('Content-Type', 'image/png')
        return response

    except Exception as e:
        print('error: {}'.format(e))

        # If no graphviz definition or bad graphviz def, return 400
        if 'syntax' in str(e):
            return make_response('Bad Request: {}'.format(e), 400)

        return make_response('Internal Server Error', 500)


# Helper function that generates a diagram based
# on a graphviz DOT diagram description.
def __create_diagram(dot):
    if not dot:
        raise Exception('syntax: no graphviz definition provided')

    dot_args = [  # These args add a watermark to the dot graphic.
        '-Glabel=Made on Cloud Functions',
        '-Gfontsize=10',
        '-Glabeljust=right',
        '-Glabelloc=bottom',
        '-Gfontcolor=gray',
        '-Tpng',
    ]

    # Uses local `dot` binary from Graphviz:
    # https://graphviz.gitlab.io
    image = subprocess.run(
        ['dot'] + dot_args, input=dot.encode('utf-8'), stdout=subprocess.PIPE
    ).stdout

    if not image:
        raise Exception('syntax: bad graphviz definition provided')
    return image
# [END functions_custom_dependencies]