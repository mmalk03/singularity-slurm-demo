import os
import subprocess
import time
from typing import Optional, Tuple

import portpicker
import requests


class VllmServer:
    def __init__(self, model_id: str, custom_args: Tuple[str, ...] = ()):
        port = portpicker.pick_unused_port()
        self.api_key = "NOT-USED"
        self.url = f"http://localhost:{port}"
        self.process = self._popen_vllm_serve(
            model_id=model_id,
            url=self.url,
            timeout=7200,
            api_key=self.api_key,
            other_args=(
                "--port",
                str(port),
                "--trust-remote-code",
                *custom_args,
            ),
            env=os.environ.copy(),
        )

    def _popen_vllm_serve(
        self,
        model_id: str,
        url: str,
        timeout: float,
        api_key: str,
        other_args: tuple = (),
        env: Optional[dict] = None,
        return_stdout_stderr: bool = False,
    ):
        command = ["vllm", "serve", model_id, "--api-key", api_key, *other_args]
        if return_stdout_stderr:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
            )
        else:
            process = subprocess.Popen(command, stdout=None, stderr=None, env=env)

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                headers = {
                    "Content-Type": "application/json; charset=utf-8",
                    "Authorization": f"Bearer {api_key}",
                }
                response = requests.get(f"{url}/v1/models", headers=headers)
                if response.status_code == 200:
                    return process
            except requests.RequestException:
                pass
            time.sleep(10)
        raise TimeoutError("Server failed to start within the timeout period.")
