/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ProjectConfig_Output } from './ProjectConfig_Output';
/**
 * continue.dev project model.
 */
export type ContinueDevProject = {
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
    config: ProjectConfig_Output;
    /**
     * Invite ID
     */
    invite_id?: string;
};

