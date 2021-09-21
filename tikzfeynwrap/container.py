__version__ = "0.0.9"

import docker
from docker.models.containers import Container
import os
import logging

logger = logging.getLogger('tikzwrapper')

from .folder import create_cache, clear_cache as _clear_cache, create_record, DEFAULT_LOCATION

class TikzFeynWrap:

    @property
    def name(self):
        if self.version:
            return self.image + ":" + self.version
        else:
            return self.image

    def __init__(
        self, 
        image="ghcr.io/npapapietro/tikzfeynwrap",
        version=__version__,
        clear_cache=False):
        self.client = docker.from_env()
        self.version = version
        self.image = image
        self.container=None

        if clear_cache:
            _clear_cache()
        else:
            create_cache()

    def check(self):
        """Performs test to see if the current sha is present
        pull if not."""
        try:
            return self.client.images.get(self.name)
        except docker.errors.ImageNotFound:
            logger.info("Getting image")
            return self.client.images.pull(self.name)

    def startup(self):
        """Performs startup actions by pulling image, cleaning up containers
        from bad exits and starting the container."""
        self.check()
        self.cleanup() # bad exit

        logger.info("Starting tikzfeynwrapper container")
        self.container: Container = self.client.containers.run(
            self.name,
            volumes = [DEFAULT_LOCATION + ":" + "/app/bind"],
            detach=True
        )
        return self

    def cleanup(self):
        """If this code exited ungracefully, cleaning up 
        dangling container"""
        for c in self.client.containers.list():
            if any(x  == self.name for x in c.image.tags):
                logger.info("Stopping tikzfeynwrapper container")
                c.stop()
                c.remove()

    def __del__(self):
        self.container.stop()
        self.container.remove()

    def __call__(self, tex: str, return_path=False, return_output=False, display=True):        
        """Runs exec against running container creating feynman diagram. Returns
        filepath if `return_path` is True.

        Args:
            tex (str): Latex of tikz-feynman compat string
            return_path (bool, optional): Returns the file path of the svg. Defaults to False.
            return_output (bool, optional): Returns the docker exec output. Defaults to False.
            display (bool, optional): Used in Jupyter Notebooks, will call `display` on svgpath. Defaults to True.
        """
        id_ = create_record()

        res = self.container.exec_run(
            ["/app/run", tex, id_],
        )

        out_path = os.path.join(DEFAULT_LOCATION, id_, 'output.svg')

        output = []
        if return_path is True:
            output.append(out_path)
        if return_output is True:
            output.append(res)

        if display:
            from IPython.display import SVG, display
            display(SVG(out_path))

        return tuple(output) if len(output) > 0 else None