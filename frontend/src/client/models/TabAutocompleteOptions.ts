/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type TabAutocompleteOptions = {
    /**
     * Disable autocomplete
     */
    disable?: (boolean | null);
    /**
     * Use copy buffer data in query
     */
    useCopyBuffer?: (boolean | null);
    /**
     * Use file suffix in query
     */
    use_file_suffix?: (boolean | null);
    /**
     * Max tokens in query
     */
    maxPromptTokens?: (number | null);
    /**
     * Time delay after last keystroke
     */
    debounceDelay?: (number | null);
    /**
     * Max suffix percentage
     */
    maxSuffixPercentage?: (number | null);
    /**
     * Prefix percentage
     */
    prefixPercentage?: (number | null);
    /**
     * Template
     */
    template?: (string | null);
    /**
     * Multiline completions
     */
    multilineCompletions?: ('always' | 'never' | 'auto' | null);
    /**
     * Use cache
     */
    useCache?: (boolean | null);
    /**
     * Only my code
     */
    onlyMyCode?: (boolean | null);
    /**
     * Use other files
     */
    useOtherFiles?: (boolean | null);
    /**
     * Disable in files
     */
    disableInFiles?: (Array<string> | null);
};

