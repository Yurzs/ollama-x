/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { APIError } from '../models/APIError';
import type { ContinueConfig } from '../models/ContinueConfig';
import type { ContinueDevProject } from '../models/ContinueDevProject';
import type { CreateProjectRequest } from '../models/CreateProjectRequest';
import type { EmbeddingsProvider } from '../models/EmbeddingsProvider';
import type { JoinResult } from '../models/JoinResult';
import type { Model_Literal__ollama___ } from '../models/Model_Literal__ollama___';
import type { TabAutocompleteModel } from '../models/TabAutocompleteModel';
import type { TabAutocompleteOptions } from '../models/TabAutocompleteOptions';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ContinueService {
    /**
     * List Projects
     * Get list of continue.dev projects.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static listProjects(): CancelablePromise<(Array<ContinueDevProject> | APIError)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/continue.all',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
            },
        });
    }
    /**
     * Get Project
     * Get information about single continue.dev project.
     * @param projectName
     * @returns ContinueDevProject Successful Response
     * @throws ApiError
     */
    public static getProject(
        projectName: string,
    ): CancelablePromise<ContinueDevProject> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/continue.one',
            query: {
                'project_name': projectName,
            },
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create new continue.dev project.
     * Create new continue.dev project.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createProject(
        requestBody: CreateProjectRequest,
    ): CancelablePromise<(ContinueDevProject | APIError)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/continue.create',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Continue Join
     * Join project by token.
     * @param inviteId
     * @param userKey
     * @returns any Successful Response
     * @throws ApiError
     */
    public static continueJoin(
        inviteId: string,
        userKey: string,
    ): CancelablePromise<(JoinResult | APIError)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/continue/join/{{invite_id}}',
            query: {
                'invite_id': inviteId,
                'user_key': userKey,
            },
            errors: {
                400: `Generic Errors.`,
                403: `Access errors.`,
                404: `Not found errors.`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get project config.
     * Get project config.
     * @returns ContinueConfig Successful Response
     * @throws ApiError
     */
    public static getConfig(): CancelablePromise<ContinueConfig> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/continue/sync',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
            },
        });
    }
    /**
     * Get project config.
     * Resets invite id in project.
     * @param projectId
     * @returns ContinueDevProject Successful Response
     * @throws ApiError
     */
    public static resetInviteId(
        projectId: string,
    ): CancelablePromise<ContinueDevProject> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/continue.reset-invite-id',
            query: {
                'project_id': projectId,
            },
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Edit Models
     * Edit project models.
     * @param projectId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static editModels(
        projectId: string,
        requestBody?: (Array<Model_Literal__ollama___> | null),
    ): CancelablePromise<(ContinueDevProject | APIError)> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/continue/models.edit',
            query: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Edit Embeddings
     * Edit project embeddings.
     * @param projectId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static editEmbeddings(
        projectId: string,
        requestBody?: (EmbeddingsProvider | null),
    ): CancelablePromise<(ContinueDevProject | APIError)> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/continue/embeddings.edit',
            query: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Edit Tab Autocomplete Model
     * Edit project tab autocomplete model.
     * @param projectId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static editTabAutocompleteModel(
        projectId: string,
        requestBody?: (TabAutocompleteModel | null),
    ): CancelablePromise<(ContinueDevProject | APIError)> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/continuetab-autocomplete-model.edit',
            query: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Edit Tab Autocomplete Options
     * Edit project tab autocomplete options.
     * @param projectId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static editTabAutocompleteOptions(
        projectId: string,
        requestBody?: (TabAutocompleteOptions | null),
    ): CancelablePromise<(ContinueDevProject | APIError)> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/continue/tab-autocomplete-options.edit',
            query: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Edit Context Providers
     * Edit project context providers.
     * @param projectId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static editContextProviders(
        projectId: string,
        requestBody?: null,
    ): CancelablePromise<(ContinueDevProject | APIError)> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/continue/context-providers.edit',
            query: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }
}
