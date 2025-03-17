/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ListAllModelsResponse } from '../models/ListAllModelsResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class OllamaService {
    /**
     * Proxy
     * Proxy generate request.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static proxy(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/chat',
        });
    }
    /**
     * Proxy
     * Proxy generate request.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static proxy1(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/generate',
        });
    }
    /**
     * Proxy
     * Proxy generate request.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static proxy2(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/ollama/api/chat',
        });
    }
    /**
     * Proxy
     * Proxy generate request.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static proxy3(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/ollama/api/generate',
        });
    }
    /**
     * Proxy
     * Proxy generate request.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static proxy4(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/ollama/v1/completions',
        });
    }
    /**
     * Proxy
     * Proxy generate request.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static proxy5(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/ollama/v1/chat/completions',
        });
    }
    /**
     * List All Models With Details
     * Get detailed information about all models installed on Ollama servers.
     * @returns ListAllModelsResponse Successful Response
     * @throws ApiError
     */
    public static listAllModelsWithDetails(): CancelablePromise<ListAllModelsResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/ollama/models',
        });
    }
}
