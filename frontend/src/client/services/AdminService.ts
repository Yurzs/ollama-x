/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { APIError } from '../models/APIError';
import type { APIServer } from '../models/APIServer';
import type { CreateUserRequest } from '../models/CreateUserRequest';
import type { OllamaListModelsResponse } from '../models/OllamaListModelsResponse';
import type { User } from '../models/User';
import type { UserBase } from '../models/UserBase';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AdminService {
    /**
     * Get user by username
     * Get users.
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getUser(
        username?: string,
    ): CancelablePromise<(User | APIError)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user.one',
            query: {
                'username': username,
            },
            errors: {
                403: `Access errors`,
                404: `Not found errors`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get all users
     * Get users from database.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllUsers(): CancelablePromise<(Array<User> | APIError)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user.all',
            errors: {
                403: `Access errors`,
            },
        });
    }
    /**
     * Create user
     * Create new user.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createUser(
        requestBody: CreateUserRequest,
    ): CancelablePromise<(UserBase | APIError)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/user.create',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Generic errors`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete user
     * Delete user by username.
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteUser(
        username: string,
    ): CancelablePromise<(User | APIError)> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/user.delete',
            query: {
                'username': username,
            },
            errors: {
                403: `Access errors`,
                404: `Not found errors`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset user API key
     * Change user key by username.
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static changeKey(
        username: string,
    ): CancelablePromise<(UserBase | APIError)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/user.reset_key',
            query: {
                'username': username,
            },
            errors: {
                403: `Access errors`,
                404: `Not found errors`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Server
     * Get server.
     * @param serverId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getServer(
        serverId: string,
    ): CancelablePromise<(APIServer | APIError)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/server.one',
            query: {
                'server_id': serverId,
            },
            errors: {
                400: `Generic errors.`,
                403: `Access errors.`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Servers
     * Get servers.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getServers(): CancelablePromise<(Array<APIServer> | APIError)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/server.all',
            errors: {
                400: `Generic errors.`,
                403: `Access errors.`,
            },
        });
    }
    /**
     * Create Server
     * Create server.
     * @param url
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createServer(
        url: string,
    ): CancelablePromise<(APIServer | APIError)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/server.create',
            query: {
                'url': url,
            },
            errors: {
                400: `Generic errors.`,
                403: `Access errors.`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Server
     * Update server parameters.
     * @param serverId
     * @param serverUrl
     * @returns APIServer Successful Response
     * @throws ApiError
     */
    public static updateServer(
        serverId: string,
        serverUrl?: (string | null),
    ): CancelablePromise<APIServer> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/server.update',
            query: {
                'server_id': serverId,
                'server_url': serverUrl,
            },
            errors: {
                400: `Generic errors.`,
                403: `Access errors.`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Server
     * Delete server.
     * @param serverId
     * @returns APIServer Successful Response
     * @throws ApiError
     */
    public static deleteServer(
        serverId: string,
    ): CancelablePromise<APIServer> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/server.delete',
            query: {
                'server_id': serverId,
            },
            errors: {
                400: `Generic errors.`,
                403: `Access errors.`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Server Models
     * Get all models for a specific server.
     * @param serverId
     * @returns OllamaListModelsResponse Successful Response
     * @throws ApiError
     */
    public static serverModels(
        serverId: string,
    ): CancelablePromise<OllamaListModelsResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/server/{server_id}/model.list',
            path: {
                'server_id': serverId,
            },
            errors: {
                400: `Generic errors.`,
                403: `Access errors.`,
                422: `Validation Error`,
            },
        });
    }
}
