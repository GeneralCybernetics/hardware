#!/usr/bin/env bash
set -eo pipefail
ROOT="$(dirname "$(realpath "$0")")/.."
AVAILABLE_PROJECTS="$(ls "$ROOT"/src)"

if [ "$#" -ne 2 ]; then
    echo "Error: Expected an argument for the project name and for the subproject name"
    echo "The project is the research objective and the subproject name contains the source files for the specific tool or piece of hardware that achieves that objective. E.g. bioelectric_cell_reprogramming/ion_concentration_biomodulator"
    echo "Usage: $0 <project_name> <subproject_name>"
    printf "Available Projects:\n%s" "$AVAILABLE_PROJECTS"
    exit 1
fi

PROJECT_NAME="$1"
SUBPROJECT_NAME="$2"
PROJECT_PATH="$ROOT/src/$PROJECT_NAME"
SUBPROJECT_PATH="$PROJECT_PATH/$SUBPROJECT_NAME"
COMMON_PATH="$(realpath "$ROOT/common")"


if [ ! -d "$PROJECT_PATH" ]; then
    echo "Project $PROJECT_NAME does not exist. Creating src/$PROJECT_NAME..."
    mkdir "$PROJECT_PATH"
fi

if [ -f "$SUBPROJECT_NAME" ]; then
    echo "Error: file $SUBPROJECT_PATH already exists. Aborting..."
    exit 1
else
    mkdir "$SUBPROJECT_PATH"
fi

cd "$SUBPROJECT_PATH" || exit 1

mkdir "$SUBPROJECT_PATH/kicad"
mkdir "$SUBPROJECT_PATH/docs"
echo "### $PROJECT_NAME $SUBPROJECT_NAME" > "$SUBPROJECT_PATH/README.md"

# symlink JLCPCB design rules, footprint libraries and symbol libraries to kicad folder
ln -s "$(realpath "$COMMON_PATH/kicad/fp-lib-table")" "$(realpath "$SUBPROJECT_PATH/kicad")"
ln -s "$(realpath "$COMMON_PATH/kicad/sym-lib-table")" "$(realpath "$SUBPROJECT_PATH/kicad")"
ln -s "$(realpath "$COMMON_PATH/kicad/JLCPCB.kicad_dru")" "$(realpath "$SUBPROJECT_PATH/kicad")"

# create boilerplate kicad project
UUID="$(uuidgen)"
sed "s/{{UUID}}/$UUID/g" "$COMMON_PATH/kicad/boilerplate/boilerplate.kicad_pro" > "$SUBPROJECT_PATH/kicad/$SUBPROJECT_NAME.kicad_pro"
sed "s/{{UUID}}/$UUID/g" "$COMMON_PATH/kicad/boilerplate/boilerplate.kicad_sch" > "$SUBPROJECT_PATH/kicad/$SUBPROJECT_NAME.kicad_sch"
cp "$COMMON_PATH/kicad/boilerplate/boilerplate.kicad_pcb" "$SUBPROJECT_PATH/kicad/$SUBPROJECT_NAME.kicad_pcb"

echo "Created kicad project at $SUBPROJECT_PATH/kicad/$SUBPROJECT_NAME.kicad_pro"