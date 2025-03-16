/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
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
}
