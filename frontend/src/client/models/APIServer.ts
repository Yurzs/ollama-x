/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ollama_x__client__ollama__OllamaModel } from './ollama_x__client__ollama__OllamaModel';
import type { OllamaRunningModel } from './OllamaRunningModel';
/**
 * Ollama API server model.
 */
export type APIServer = {
    /**
     * Server API base URL
     */
    url: string;
    _id?: string;
    /**
     * Last update
     */
    last_update?: string;
    /**
     * Last alive
     */
    last_alive?: string;
    /**
     * Models
     */
    models?: Array<ollama_x__client__ollama__OllamaModel>;
    /**
     * Running models
     */
    running_models?: Array<OllamaRunningModel>;
};

