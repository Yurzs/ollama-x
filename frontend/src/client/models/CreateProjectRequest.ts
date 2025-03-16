/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ProjectConfig_Input } from './ProjectConfig_Input';
/**
 * Request to create a new project.
 */
export type CreateProjectRequest = {
    _id?: string;
    /**
     * Project admin
     */
    admin: string;
    /**
     * Project name
     */
    name: string;
    /**
     * Project users
     */
    users?: Array<string>;
    /**
     * continue.dev project config
     */
    config: ProjectConfig_Input;
    /**
     * Invite ID
     */
    invite_id?: string;
};

