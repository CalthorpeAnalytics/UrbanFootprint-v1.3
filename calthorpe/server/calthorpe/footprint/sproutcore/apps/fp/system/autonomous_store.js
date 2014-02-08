// SC.Store (for autonomous nested stores)
SC.Store.reopen({
  chainAutonomousStore: function(attrs, newStoreClass) {
    var newAttrs = attrs ? SC.clone( attrs ) : {};
    var source  = this._getDataSource();

    newAttrs.dataSource = source;
    return this.chain( newAttrs, newStoreClass );
  }
});

// SC.NestedStore (for autonomous nested stores)
SC.NestedStore.reopen({
  chainAutonomousStore: function(attrs, newStoreClass) {
    throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  commitRecords: function(recordTypes, ids, storeKeys) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  commitRecord: function(recordType, id, storeKey) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  cancelRecords: function(recordTypes, ids, storeKeys) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  cancelRecord: function(recordType, id, storeKey) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  dataSourceDidCancel: function(storeKey) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  dataSourceDidComplete: function(storeKey, dataHash, newId) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  dataSourceDidDestroy: function(storeKey) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  dataSourceDidError: function(storeKey, error) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  pushRetrieve: function(recordType, id, dataHash, storeKey) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  pushDestroy: function(recordType, id, storeKey) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  },
  pushError: function(recordType, id, error, storeKey) {
    if( this.get( "dataSource" ) )
      return sc_super();
    else
      throw SC.Store.NESTED_STORE_UNSUPPORTED_ERROR;
  }
  
});
