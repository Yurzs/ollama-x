from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.user import User
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    username: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_username: Union[None, Unset, str]
    if isinstance(username, Unset):
        json_username = UNSET
    else:
        json_username = username
    params["username"] = json_username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/user/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Union["User", List["User"]]]]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(data: object) -> Union["User", List["User"]]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = User.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            response_200_type_1 = []
            _response_200_type_1 = data
            for response_200_type_1_item_data in _response_200_type_1:
                response_200_type_1_item = User.from_dict(response_200_type_1_item_data)

                response_200_type_1.append(response_200_type_1_item)

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
) -> Response[Union[HTTPValidationError, Union["User", List["User"]]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    username: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, Union["User", List["User"]]]]:
    """Get all users or user by username

     Get users.

    Args:
        username (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['User', List['User']]]]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    username: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, Union["User", List["User"]]]]:
    """Get all users or user by username

     Get users.

    Args:
        username (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['User', List['User']]]
    """

    return sync_detailed(
        client=client,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    username: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, Union["User", List["User"]]]]:
    """Get all users or user by username

     Get users.

    Args:
        username (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['User', List['User']]]]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    username: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, Union["User", List["User"]]]]:
    """Get all users or user by username

     Get users.

    Args:
        username (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['User', List['User']]]
    """

    return (
        await asyncio_detailed(
            client=client,
            username=username,
        )
    ).parsed
