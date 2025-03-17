/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseCompletionOptions } from './BaseCompletionOptions';
import type { RequestOptions } from './RequestOptions';
export type TabAutocompleteModel = {
    /**
     * OllamaModel title
     */
    title?: string;
    /**
     * Provider
     */
    provider?: string;
    /**
     * OllamaModel name
     */
    model: string;
    /**
     * API key
     */
    apiKey?: (string | null);
    /**
     * API base
     */
    apiBase?: (string | null);
    /**
     * Context length
     */
    contextLength?: (number | null);
    /**
     * Template
     */
    template?: (string | null);
    /**
     * Prompt templates
     */
    promptTemplates?: (Record<string, string> | null);
    /**
     * Completion options
     */
    completionOptions?: (BaseCompletionOptions | null);
    /**
     * Request options
     */
    requestOptions?: RequestOptions;
};

