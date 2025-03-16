/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RequestOptions } from './RequestOptions';
export type EmbeddingsProvider = {
    /**
     * Provider name
     */
    provider?: string;
    /**
     * OllamaModel name
     */
    model?: (string | null);
    /**
     * API base
     */
    apiBase?: (string | null);
    /**
     * API key
     */
    apiKey?: (string | null);
    /**
     * Request options
     */
    requestOptions?: RequestOptions;
};

