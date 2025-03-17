/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OllamaModelDetails } from './OllamaModelDetails';
export type OllamaRunningModel = {
    name: string;
    model: string;
    size: number;
    digest: string;
    details: OllamaModelDetails;
    expires_at: string;
    size_vram: number;
};

