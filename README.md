# number-graph
Loading number word length graphs into Neo4j

```cypher
MATCH (n1:Number)
WHERE (n1)<-[:LINK {lang: "eo"}]-(:Number)
OPTIONAL MATCH (n1)<-[e1:LINK {lang: "eo"}]-(n2:Number)
WHERE (n2)<-[:LINK {lang: "eo"}]-(:Number)
RETURN n1, e1, n2
```