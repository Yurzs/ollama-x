/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type User = {
    _id?: string;
    /**
     * Username
     */
    username: string;
    /**
     * Is user admin flag
     */
    is_admin?: boolean;
    /**
     * Is user active
     */
    is_active?: boolean;
    /**
     * Users API key
     */
    key: string;
    /**
     * Hashed password
     */
    hashed_password?: (string | null);
};

