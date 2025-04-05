from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

def fetch_frame_requests():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://localhost:3000/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
        query AgentTasksQuery {
          frameRequests {
            nodes {
              frameNumber
              renderRequest {
                archive {
                  url
                  nodeId
                }
              }
            }
          }
        }
        """
    )

    # Execute the query on the transport
    result = client.execute(query)
    print(result)
