const { ConstraintErrorTagsPlugin, handleErrors } = require("@graphile-contrib/constraint-error-tags");
const PgSimplifyInflectorPlugin = require("@graphile-contrib/pg-simplify-inflector");
const PostGraphileUploadFieldPlugin = require("postgraphile-plugin-upload-field");
const { graphqlUploadExpress } = require("graphql-upload");
const { postgraphile, makePluginHook } = require("postgraphile");
const { default: PgPubsub } = require("@graphile/pg-pubsub");
const express = require("express");

const PgPubsubPluginHook = makePluginHook([PgPubsub]);

const app = express();

const graphileOptions = {
  pluginHook: PgPubsubPluginHook,
  appendPlugins: [PgSimplifyInflectorPlugin, ConstraintErrorTagsPlugin],
  handleErrors: (errors) => handleErrors(errors),
  watchPg: true,
  graphiql: true,
  enhanceGraphiql: true,
  subscriptions: true,
  simpleSubscriptions: true,
  pgStrictFunctions: true,
};

app.use( postgraphile( process.env.DATABASE_URL, "public", graphileOptions ) );

const port =  process.env.PORT || 3000;

app.listen(port, () => {
  console.log(`listening on port ${port}`)
});
