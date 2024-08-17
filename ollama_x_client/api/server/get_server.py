from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_server import APIServer
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    server_id: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_server_id: Union[None, Unset, str]
    if isinstance(server_id, Unset):
        json_server_id = UNSET
    else:
        json_server_id = server_id
    params["server_id"] = json_server_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/server/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Union["APIServer", List["APIServer"]]]]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(data: object) -> Union["APIServer", List["APIServer"]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                response_200_type_0 = []
                _response_200_type_0 = data
                for response_200_type_0_item_data in _response_200_type_0:
                    response_200_type_0_item = APIServer.from_dict(response_200_type_0_item_data)

                    response_200_type_0.append(response_200_type_0_item)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = APIServer.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

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
) -> Response[Union[HTTPValidationError, Union["APIServer", List["APIServer"]]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    server_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, Union["APIServer", List["APIServer"]]]]:
    """Get Server

     Get server.

    Args:
        server_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['APIServer', List['APIServer']]]]
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
    server_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, Union["APIServer", List["APIServer"]]]]:
    """Get Server

     Get server.

    Args:
        server_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['APIServer', List['APIServer']]]
    """

    return sync_detailed(
        client=client,
        server_id=server_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    server_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, Union["APIServer", List["APIServer"]]]]:
    """Get Server

     Get server.

    Args:
        server_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['APIServer', List['APIServer']]]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    server_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, Union["APIServer", List["APIServer"]]]]:
    """Get Server

     Get server.

    Args:
        server_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['APIServer', List['APIServer']]]
    """

    return (
        await asyncio_detailed(
            client=client,
            server_id=server_id,
        )
    ).parsed
