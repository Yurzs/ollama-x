/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { APIError } from '../models/APIError';
import type { CreateUserRequest } from '../models/CreateUserRequest';
import type { LoginRequest } from '../models/LoginRequest';
import type { Token } from '../models/Token';
import type { User } from '../models/User';
import type { UserBase } from '../models/UserBase';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UserService {
    /**
     * Login For Access Token
     * Generate JWT token for user authentication.
     * @param requestBody
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static loginForAccessToken(
        requestBody: LoginRequest,
    ): CancelablePromise<Token> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/user.login',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Read Users Me
     * Get current user information.
     * @returns UserBase Successful Response
     * @throws ApiError
     */
    public static readUsersMe(): CancelablePromise<UserBase> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user/me',
        });
    }
    /**
     * Get user by username
     * Get users.
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getUser(
        username?: string,
    ): CancelablePromise<(User | APIError)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user.one',
            query: {
                'username': username,
            },
            errors: {
                403: `Access errors`,
                404: `Not found errors`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get all users
     * Get users from database.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllUsers(): CancelablePromise<(Array<User> | APIError)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user.all',
            errors: {
                403: `Access errors`,
            },
        });
    }
    /**
     * Create user
     * Create new user.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createUser(
        requestBody: CreateUserRequest,
    ): CancelablePromise<(UserBase | APIError)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/user.create',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Generic errors`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete user
     * Delete user by username.
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteUser(
        username: string,
    ): CancelablePromise<(User | APIError)> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/user.delete',
            query: {
                'username': username,
            },
            errors: {
                403: `Access errors`,
                404: `Not found errors`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset user API key
     * Change user key by username.
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static changeKey(
        username: string,
    ): CancelablePromise<(UserBase | APIError)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/user.reset_key',
            query: {
                'username': username,
            },
            errors: {
                403: `Access errors`,
                404: `Not found errors`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Register new user
     * Register new user.
     * @param email
     * @param password
     * @returns any Successful Response
     * @throws ApiError
     */
    public static userRegister(
        email: string,
        password: string,
    ): CancelablePromise<(UserBase | APIError)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user.register',
            query: {
                'email': email,
                'password': password,
            },
            errors: {
                400: `Generic errors`,
                403: `Access denied`,
                422: `Validation Error`,
            },
        });
    }
}
