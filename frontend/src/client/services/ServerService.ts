/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { APIError } from '../models/APIError';
import type { APIServer } from '../models/APIServer';
import type { OllamaListModelsResponse } from '../models/OllamaListModelsResponse';
import type { OllamaPullModelResponseSingle } from '../models/OllamaPullModelResponseSingle';
import type { OllamaPullModelResponseStream } from '../models/OllamaPullModelResponseStream';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ServerService {
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
    /**
     * Server Pull Model
     * Pull model to server.
     * @param serverId
     * @param model
     * @param stream
     * @returns any Successful Response
     * @throws ApiError
     */
    public static serverPullModel(
        serverId: string,
        model: string,
        stream: boolean = true,
    ): CancelablePromise<(OllamaPullModelResponseSingle | OllamaPullModelResponseStream)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/server/{server_id}/model.pull',
            path: {
                'server_id': serverId,
            },
            query: {
                'model': model,
                'stream': stream,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Server Delete Model
     * Delete model from server.
     * @param serverId
     * @param model
     * @returns any Successful Response
     * @throws ApiError
     */
    public static serverDeleteModel(
        serverId: string,
        model: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/server/{server_id}/model.delete',
            path: {
                'server_id': serverId,
            },
            query: {
                'model': model,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
