import type { CodegenConfig as BaseCodegenConfig } from '@graphql-codegen/cli';

type CodegenConfig = BaseCodegenConfig;

const config: CodegenConfig = {
  schema: [`./src/graphql/autogenerated_schema.gql`],
  documents: ['src/**/!(*.test).js*', 'src/**/!(*.test).ts*'],
  config: {
    avoidOptionals: {
      // Do not mark fields in the response as optional
      field: true,
    },
    namingConvention: {
      // Use ALL_CAPS for enum values
      enumValues: 'change-case-all#constantCase',
    },
    // Always include __typename fields on response types
    nonOptionalTypename: true,
    // Do not include "Query"/"Mutation" in the type name
    omitOperationSuffix: true,
    // Only include enums and operations to avoid introducing duplicate types
    onlyOperationTypes: true,
    // Explicitly list out mapping for custom scalars from GQL type to TS type
    scalars: {
      GraphQLAnyValue: 'any',
      Long: 'number',
      LongString: 'string',
      StringMap: 'Record<string, string>',
      JSON: 'any',
      WellKnownFieldMask: 'any',
      WellKnownTimestamp: 'any',
      WellKnownDuration: 'any',
    },
    // Omit `__typename: 'QueryType'/'MutationType'` on operation types
    skipTypeNameForRoot: true,
    // Require all custom scalars to be specified in `scalars`
    strictScalars: true,
  },
  generates: {
    'src/graphql/__generated__/graphql.ts': {
      plugins: ['graphql-codegen-typescript-operation-types', 'typescript-operations'],
    },
  },
};

// eslint-disable-next-line import/no-default-export
export default config;
