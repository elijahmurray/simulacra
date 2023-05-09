from colorama import Fore, Style
import inspect
from config import (
    ENABLE_METHOD_CALLED_LOGGING,
    ENABLE_PROMPT_LOGGING,
    ENABLE_PROMPT_CONTEXT_LOGGING,
    ENABLE_AGENT_EVENT_LOGGING,
    ENABLE_WORLD_EVENT_LOGGING,
    ENABLE_LLM_RESPONSE_LOGGING,
)


class Logger:
    def log(message: str, type: str, force_log: bool = False) -> None:
        if force_log:
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")
            return
        if type == "method" and ENABLE_METHOD_CALLED_LOGGING:
            print(
                f"{Fore.RED}\n==========================\nCALLED: {message}\n=========================={Style.RESET_ALL}"
            )
            return
        if type == "prompt" and ENABLE_PROMPT_LOGGING:
            print(f"{Fore.MAGENTA}{message}{Style.RESET_ALL}")
            return
        if type == "context" and ENABLE_PROMPT_CONTEXT_LOGGING:
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")
            return
        if type == "agent_event" and ENABLE_AGENT_EVENT_LOGGING:
            print(f"{Fore.WHITE}{message}{Style.RESET_ALL}")
            return
        if type == "world_event" and ENABLE_WORLD_EVENT_LOGGING:
            print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
            return
        if type == "llm_response" and ENABLE_LLM_RESPONSE_LOGGING:
            print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
            return
        else:
            return

    def calling_method_name() -> str:
        # get the frame object of the calling function
        frame = inspect.currentframe().f_back
        # get the code object of the calling function
        code = frame.f_code
        # get the name of the calling function
        name = code.co_name
        return name
