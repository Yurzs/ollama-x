/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ContextProvider_Literal__code___NoneType_ } from './ContextProvider_Literal__code___NoneType_';
import type { ContextProvider_Literal__codebase___NoneType_ } from './ContextProvider_Literal__codebase___NoneType_';
import type { ContextProvider_Literal__diff___NoneType_ } from './ContextProvider_Literal__diff___NoneType_';
import type { ContextProvider_Literal__docs___DocsParameters__Input } from './ContextProvider_Literal__docs___DocsParameters__Input';
import type { ContextProvider_Literal__open___OpenParameters_ } from './ContextProvider_Literal__open___OpenParameters_';
import type { ContextProvider_Literal__search___NoneType_ } from './ContextProvider_Literal__search___NoneType_';
import type { ContextProvider_Literal__url___NoneType_ } from './ContextProvider_Literal__url___NoneType_';
import type { CustomCommand } from './CustomCommand';
import type { EmbeddingsProvider } from './EmbeddingsProvider';
import type { Model_Literal__ollama___ } from './Model_Literal__ollama___';
import type { RequestOptions } from './RequestOptions';
import type { TabAutocompleteModel } from './TabAutocompleteModel';
import type { TabAutocompleteOptions } from './TabAutocompleteOptions';
export type ProjectConfig_Input = {
    /**
     * Project models
     */
    models?: Array<Model_Literal__ollama___>;
    /**
     * Custom commands
     */
    customCommands?: Array<CustomCommand>;
    /**
     * Request options
     */
    requestOptions?: RequestOptions;
    /**
     * Tab autocomplete model
     */
    tabAutocompleteModel?: (TabAutocompleteModel | Array<TabAutocompleteModel> | null);
    /**
     * Tab autocomplete options
     */
    tabAutocompleteOptions?: (TabAutocompleteOptions | null);
    /**
     * Allow anonymous telemetry
     */
    allowAnonymousTelemetry?: boolean;
    /**
     * Context providers
     */
    contextProviders?: Array<(ContextProvider_Literal__code___NoneType_ | ContextProvider_Literal__codebase___NoneType_ | ContextProvider_Literal__diff___NoneType_ | ContextProvider_Literal__docs___DocsParameters__Input | ContextProvider_Literal__open___OpenParameters_ | ContextProvider_Literal__search___NoneType_ | ContextProvider_Literal__url___NoneType_)>;
    /**
     * Embeddings provider
     */
    embeddingsProvider?: (EmbeddingsProvider | null);
};

