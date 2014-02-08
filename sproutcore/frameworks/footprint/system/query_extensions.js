/**
 * Created by calthorpe on 11/18/13.
 */

Footprint.queryLanguage = SC.clone(SC.Query.create().queryLanguage)
Footprint.queryLanguage.WHERE_COUNT = { reservedWord: YES, rightType: 'BOOLEAN', evalType: 'PRIMITIVE' }
Footprint.queryLanguage.WHERE_AVG = { reservedWord: YES, rightType: 'BOOLEAN', evalType: 'PRIMITIVE' }
Footprint.queryLanguage.WHERE_SUM = { reservedWord: YES, rightType: 'BOOLEAN', evalType: 'PRIMITIVE' }
// t = q.tokenizeString("COUNT(poster=5)", q.queryLanguage)
// tr = q.buildTokenTree(t, q.queryLanguage)
Footprint.queryLanguage.COUNT = { reservedWord: YES, rightType: 'PRIMITIVE', evalType: 'PRIMITIVE' }
Footprint.queryLanguage.AVG = { reservedWord: YES, rightType: 'PRIMITIVE', evalType: 'PRIMITIVE' }
Footprint.queryLanguage.SUM = { reservedWord: YES, rightType: 'PRIMITIVE', evalType: 'PRIMITIVE' }

Footprint.queryLanguage.AREA = { reservedWord: YES, rightType: 'PRIMITIVE', evalType: 'PRIMITIVE' }
// t = q.tokenizeString("COUNT(poster)", q.queryLanguage)
// tr = q.buildTokenTree(t, q.queryLanguage)

// Basic query handling. This will be improved
function processQuery(queryString) {
    var queryFactory = SC.Query.create();
    var tokenList = queryFactory.tokenizeString(queryString, Footprint.queryLanguage);
    if (tokenList.error)
        throw tokenList.error;
    return queryFactory.buildTokenTree(tokenList, Footprint.queryLanguage);
}
