// -*- mode: c++; coding: utf-8 -*-

module Semantic {

  exception SconeError { string reason; };
  exception FileError { string reason; };

  interface SconeService {
	// FIXME: Service* requestService(string request);
	// FIXME: "scone" is reduntant in this method:

      string request(string request) throws SconeError;
      string sentence(string sentence) throws SconeError;
      void checkpoint(string name) throws FileError;
    };
};
