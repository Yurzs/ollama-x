from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_server import APIServer
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    server_id: str,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["server_id"] = server_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": "/server/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[APIServer, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = APIServer.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[APIServer, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    server_id: str,
) -> Response[Union[APIServer, HTTPValidationError]]:
    """Delete Server

     Delete server.

    Args:
        server_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[APIServer, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    server_id: str,
) -> Optional[Union[APIServer, HTTPValidationError]]:
    """Delete Server

     Delete server.

    Args:
        server_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[APIServer, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        server_id=server_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    server_id: str,
) -> Response[Union[APIServer, HTTPValidationError]]:
    """Delete Server

     Delete server.

    Args:
        server_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[APIServer, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    server_id: str,
) -> Optional[Union[APIServer, HTTPValidationError]]:
    """Delete Server

     Delete server.

    Args:
        server_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[APIServer, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            server_id=server_id,
        )
    ).parsed
