from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, RootModel

ASSETS_DIR = Path("docs")


class Skin(BaseModel):
    chName: str
    skelName: str
    atlasName: str
    pages: List[str]


class Ship(BaseModel):
    chName: str
    hxName: Optional[str] = None
    skins: Dict[str, Skin]


class ShipData(RootModel):
    root: Dict[str, Ship]


if __name__ == "__main__":
    shipdata = ShipData.model_validate_json(ASSETS_DIR.joinpath("index.json").read_bytes(), strict=True)

    nonexisted = []
    for shipname, ship in shipdata.root.items():
        shipd = ASSETS_DIR.joinpath(shipname)

        for skinname, skin in ship.skins.items():
            skelpath = shipd.joinpath(skin.skelName)
            if not skelpath.is_file():
                nonexisted.append(skelpath)

            atlaspath = shipd.joinpath(skin.atlasName)
            if not atlaspath.is_file():
                nonexisted.append(atlaspath)

            for page in skin.pages:
                pagepath = shipd.joinpath(page)
                if not pagepath.is_file():
                    nonexisted.append(pagepath)

    if len(nonexisted) > 0:
        raise FileNotFoundError(nonexisted)

    existed = []
    for shipd in ASSETS_DIR.iterdir():
        if not shipd.is_dir() or shipd.name.startswith("."):
            continue

        shipname = shipd.name
        ship = shipdata.root.get(shipname)
        if ship is None:
            existed.append(shipd)
            continue

        valid_filenames = []
        valid_filenames.extend(skin.skelName for skin in ship.skins.values())
        valid_filenames.extend(skin.atlasName for skin in ship.skins.values())
        valid_filenames.extend(pagepath for skin in ship.skins.values() for pagepath in skin.pages)

        for path in shipd.iterdir():
            if path.name not in valid_filenames:
                existed.append(path)

    if len(existed) > 0:
        raise FileExistsError(existed)
