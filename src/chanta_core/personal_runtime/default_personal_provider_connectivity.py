"""v0.42.7 configured provider connectivity and chat UX stabilization.

This module adds a bounded no-completion ``/models`` probe and CLI
stabilization glue. It does not add provider tools, function calling, shell
execution, subagents, file edit/apply, autonomous loops, or production
certification.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, is_dataclass
from enum import StrEnum
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_diagnostics_feedback import main as _v0426_main
from chanta_core.personal_runtime.default_personal_home_quickstart import (
    PROFILE_ID,
    create_v042_home_resolution_request,
    resolve_v042_home,
)
from chanta_core.personal_runtime.default_personal_provider_skills import (
    ProviderConfig,
    load_provider_config_from_profile,
)


V0427_VERSION = "v0.42.7"
V0427_RELEASE_NAME = "v0.42.7 Configured Provider Connectivity & Chat UX Stabilization"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.7_provider_connectivity_chat_ux_stabilization_restore.md"


class V0427ProviderConnectivityStatus(StrEnum):
    PASS_ = "pass"
    FAIL = "fail"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class V0427ProviderConnectivityErrorClass(StrEnum):
    NONE = "none"
    ENDPOINT_UNREACHABLE = "endpoint_unreachable"
    CONNECTION_REFUSED = "connection_refused"
    MODELS_ENDPOINT_TIMEOUT = "models_endpoint_timeout"
    MODEL_NOT_FOUND = "model_not_found"
    INVALID_MODELS_RESPONSE = "invalid_models_response"
    AUTH_REQUIRED = "auth_required"
    REMOTE_PROBE_BLOCKED = "remote_probe_blocked"
    UNKNOWN_PROVIDER_ERROR = "unknown_provider_error"


@dataclass(frozen=True)
class V0427ProviderConnectivityRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    timeout_seconds: float
    allow_remote_probe: bool


@dataclass(frozen=True)
class V0427ProviderConnectivityResult:
    result_id: str
    profile_id: str
    resolved_home_path: str
    base_url: str | None
    configured_model: str | None
    endpoint_reachable: bool
    models_endpoint_reachable: bool
    model_list_available: bool
    configured_model_found: bool
    available_model_ids: tuple[str, ...]
    timeout_seconds: float
    error_class: str
    next_action: str
    rendered_text: str
    completion_endpoint_called: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V0427StabilizationSafetyReport:
    report_id: str
    provider_doctor_completion_opened: bool
    provider_tool_calling_opened: bool
    function_calling_opened: bool
    shell_execution_opened: bool
    subagent_invocation_opened: bool
    general_agent_loop_opened: bool
    retry_loop_opened: bool
    production_certified: bool


def _merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _json_ready(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    return value


def _render_json(value: Any) -> str:
    return json.dumps(_json_ready(value), indent=2, sort_keys=True)


def _resolve_home(home_path: str | None, command_name: str) -> str:
    result = resolve_v042_home(create_v042_home_resolution_request(explicit_home=home_path, command_name=command_name))
    return result.home_path if result.safe_to_use else ""


def _provider_url(base_url: str, endpoint_path: str) -> str:
    parsed = urllib.parse.urlparse(base_url)
    safe = parsed._replace(params="", query="", fragment="")
    return urllib.parse.urljoin(urllib.parse.urlunparse(safe).rstrip("/") + "/", endpoint_path.lstrip("/"))


def _is_loopback(base_url: str | None) -> bool:
    if not base_url:
        return False
    host = urllib.parse.urlparse(base_url).hostname
    return host in {"localhost", "127.0.0.1", "::1"}


def _classify_models_error(exc: BaseException) -> str:
    if isinstance(exc, urllib.error.HTTPError) and exc.code in {401, 403}:
        return V0427ProviderConnectivityErrorClass.AUTH_REQUIRED.value
    text = str(exc).lower()
    reason = getattr(exc, "reason", None)
    reason_text = str(reason).lower() if reason is not None else ""
    combined = f"{text} {reason_text}"
    if isinstance(exc, TimeoutError) or "timed out" in combined or "timeout" in combined:
        return V0427ProviderConnectivityErrorClass.MODELS_ENDPOINT_TIMEOUT.value
    if "connection refused" in combined or "actively refused" in combined or "winerror 10061" in combined:
        return V0427ProviderConnectivityErrorClass.CONNECTION_REFUSED.value
    return V0427ProviderConnectivityErrorClass.UNKNOWN_PROVIDER_ERROR.value


def _model_ids_from_response(raw_text: str) -> tuple[str, ...] | None:
    data = json.loads(raw_text)
    models = data.get("data") if isinstance(data, dict) else data
    if not isinstance(models, list):
        return None
    ids: list[str] = []
    for item in models:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            ids.append(item["id"])
        elif isinstance(item, str):
            ids.append(item)
    return tuple(ids)


def create_v0427_provider_connectivity_request(
    home_path: str | None = None,
    profile_id: str = PROFILE_ID,
    timeout_seconds: float = 5.0,
    allow_remote_probe: bool = False,
    **overrides: Any,
) -> V0427ProviderConnectivityRequest:
    defaults = {
        "request_id": "v0427-provider-connectivity-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "timeout_seconds": max(1.0, min(float(timeout_seconds), 30.0)),
        "allow_remote_probe": allow_remote_probe,
    }
    return V0427ProviderConnectivityRequest(**_merge(defaults, overrides))


def probe_v0427_provider_connectivity(
    request: V0427ProviderConnectivityRequest,
    *,
    urlopen: Any | None = None,
) -> V0427ProviderConnectivityResult:
    home = _resolve_home(request.home_path, "provider connectivity")
    config: ProviderConfig | None = load_provider_config_from_profile(home) if home else None
    base_url = config.base_url if config else None
    model = config.model if config else None
    opener = urllib.request.urlopen if urlopen is None else urlopen
    endpoint_reachable = False
    models_reachable = False
    available_ids: tuple[str, ...] = ()
    error_class = V0427ProviderConnectivityErrorClass.NONE.value

    if not home or not base_url or not model:
        error_class = V0427ProviderConnectivityErrorClass.ENDPOINT_UNREACHABLE.value
    elif not request.allow_remote_probe and not _is_loopback(base_url):
        error_class = V0427ProviderConnectivityErrorClass.REMOTE_PROBE_BLOCKED.value
    else:
        models_url = _provider_url(base_url, "/models")
        http_request = urllib.request.Request(models_url, headers={"Accept": "application/json"}, method="GET")
        try:
            with opener(http_request, timeout=request.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
            ids = _model_ids_from_response(raw)
            endpoint_reachable = True
            models_reachable = True
            if ids is None:
                error_class = V0427ProviderConnectivityErrorClass.INVALID_MODELS_RESPONSE.value
            else:
                available_ids = ids
                error_class = V0427ProviderConnectivityErrorClass.NONE.value if model in available_ids else V0427ProviderConnectivityErrorClass.MODEL_NOT_FOUND.value
        except json.JSONDecodeError:
            endpoint_reachable = True
            models_reachable = True
            error_class = V0427ProviderConnectivityErrorClass.INVALID_MODELS_RESPONSE.value
        except (urllib.error.URLError, TimeoutError) as exc:
            error_class = _classify_models_error(exc)

    found = bool(model and model in available_ids)
    next_action = _next_action_for_connectivity(error_class, model)
    rendered = _render_connectivity_text(home, base_url, model, endpoint_reachable, models_reachable, available_ids, found, request.timeout_seconds, error_class, next_action)
    return V0427ProviderConnectivityResult(
        result_id="v0427-provider-connectivity-result",
        profile_id=request.profile_id,
        resolved_home_path=home,
        base_url=base_url,
        configured_model=model,
        endpoint_reachable=endpoint_reachable,
        models_endpoint_reachable=models_reachable,
        model_list_available=bool(available_ids),
        configured_model_found=found,
        available_model_ids=available_ids,
        timeout_seconds=request.timeout_seconds,
        error_class=error_class,
        next_action=next_action,
        rendered_text=rendered,
        completion_endpoint_called=False,
        provider_invoked=False,
        prompt_submitted=False,
        shell_executed=False,
        subagent_invoked=False,
        production_certified=False,
    )


def _next_action_for_connectivity(error_class: str, model: str | None) -> str:
    if error_class == V0427ProviderConnectivityErrorClass.NONE.value:
        return "configured provider metadata endpoint is reachable; try chanta-cli run --provider configured"
    if error_class == V0427ProviderConnectivityErrorClass.MODEL_NOT_FOUND.value:
        return f"set --model to one of the available /models ids; configured model was {model or '(none)'}"
    if error_class in {V0427ProviderConnectivityErrorClass.CONNECTION_REFUSED.value, V0427ProviderConnectivityErrorClass.ENDPOINT_UNREACHABLE.value}:
        return "start LM Studio/local server and confirm base_url, then rerun provider connectivity"
    if error_class == V0427ProviderConnectivityErrorClass.MODELS_ENDPOINT_TIMEOUT.value:
        return "increase --timeout or check whether the local provider server is responsive"
    if error_class == V0427ProviderConnectivityErrorClass.AUTH_REQUIRED.value:
        return "set the configured environment variable without storing the secret in ChantaCore"
    if error_class == V0427ProviderConnectivityErrorClass.REMOTE_PROBE_BLOCKED.value:
        return "remote provider metadata probe is blocked by default; use loopback/local endpoint"
    return "inspect provider config and rerun provider connectivity"


def _render_connectivity_text(
    home: str,
    base_url: str | None,
    model: str | None,
    endpoint_reachable: bool,
    models_reachable: bool,
    available_ids: tuple[str, ...],
    found: bool,
    timeout: float,
    error_class: str,
    next_action: str,
) -> str:
    return "\n".join(
        (
            "ChantaCore provider connectivity",
            f"  resolved_home: {home or '(unresolved)'}",
            f"  base_url: {base_url or '(none)'}",
            f"  configured_model: {model or '(none)'}",
            f"  endpoint_reachable: {str(endpoint_reachable).lower()}",
            f"  models_endpoint_reachable: {str(models_reachable).lower()}",
            f"  model_list_available: {str(bool(available_ids)).lower()}",
            f"  configured_model_found: {str(found).lower()}",
            f"  available_model_ids: {', '.join(available_ids) if available_ids else '(none)'}",
            f"  timeout_seconds: {timeout:g}",
            f"  error_class: {error_class}",
            "  completion_endpoint_called: false",
            "  provider_invoked: false",
            "  prompt_submitted: false",
            "  shell_executed: false",
            "  subagent_invoked: false",
            "  production_certified: false",
            f"  next: {next_action}",
        )
    )


def create_v0427_stabilization_safety_report(**overrides: Any) -> V0427StabilizationSafetyReport:
    defaults = {
        "report_id": "v0427-stabilization-safety-report",
        "provider_doctor_completion_opened": False,
        "provider_tool_calling_opened": False,
        "function_calling_opened": False,
        "shell_execution_opened": False,
        "subagent_invocation_opened": False,
        "general_agent_loop_opened": False,
        "retry_loop_opened": False,
        "production_certified": False,
    }
    return V0427StabilizationSafetyReport(**_merge(defaults, overrides))


def _print_run_help() -> None:
    parser = argparse.ArgumentParser(prog="chanta-cli run", description="Run one explicit single-turn text prompt.")
    parser.add_argument("--profile", default=PROFILE_ID, help="profile id")
    parser.add_argument("--home", help="ChantaCore home path; may be resolved from CHANTACORE_HOME/default home")
    parser.add_argument("--session", help="session id to append on successful provider response")
    parser.add_argument("--provider", choices=["mock", "configured"], default=None, help="provider mode")
    parser.add_argument("--timeout", type=float, help="configured provider timeout seconds")
    parser.add_argument("prompt", help="single explicit user prompt")
    parser.print_help()


def _handle_provider_connectivity(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli provider connectivity")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--allow-remote-probe", action="store_true")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    result = probe_v0427_provider_connectivity(
        create_v0427_provider_connectivity_request(parsed.home, parsed.profile, parsed.timeout, parsed.allow_remote_probe)
    )
    print(_render_json(result) if parsed.json else result.rendered_text)
    return 0 if result.error_class in {V0427ProviderConnectivityErrorClass.NONE.value, V0427ProviderConnectivityErrorClass.MODEL_NOT_FOUND.value} else 1


def _run_args_with_resolved_home(args: Sequence[str]) -> list[str]:
    if "--home" in args or "-h" in args or "--help" in args:
        return list(args)
    home = _resolve_home(None, "run")
    if not home:
        return list(args)
    return [args[0], "--home", home, *args[1:]]


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0427_VERSION}; {V0427_RELEASE_NAME})")
        return 0
    if args and args[0] == "run" and ("--help" in args or "-h" in args):
        _print_run_help()
        return 0
    if args and args[0] == "chat" and ("--help" in args or "-h" in args):
        try:
            return _v0426_main(args)
        except SystemExit as exc:
            return int(exc.code or 0)
    if args and args[0] == "run":
        return _v0426_main(_run_args_with_resolved_home(args))
    if len(args) >= 2 and args[0] == "provider" and args[1] == "connectivity":
        return _handle_provider_connectivity(args[2:])
    if len(args) >= 3 and args[0] == "provider" and args[1] == "doctor" and "--probe-models" in args:
        probe_args = [item for item in args[2:] if item not in {"--probe-models", "--no-completion"}]
        return _handle_provider_connectivity(probe_args)
    return _v0426_main(args)


__all__ = [
    name
    for name in globals()
    if name.startswith("V0427")
    or name.startswith("create_v0427")
    or name.startswith("probe_v0427")
    or name == "main"
]
