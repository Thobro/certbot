""" apacheconfig implementation of the ParserNode interfaces """

from certbot_apache._internal import assertions
from certbot_apache._internal import interfaces
from certbot_apache._internal import parsernode_util as util


class ApacheParserNode(interfaces.ParserNode):
    """ apacheconfig implementation of ParserNode interface.

        Expects metadata `ac_ast` to be passed in, where `ac_ast` is the AST provided
        by parsing the equivalent configuration text using the apacheconfig library.
    """

    def __init__(self, **kwargs):
        ancestor, dirty, filepath, metadata = util.parsernode_kwargs(kwargs)  # pylint: disable=unused-variable
        super(ApacheParserNode, self).__init__(**kwargs)
        self.ancestor = ancestor
        self.filepath = filepath
        self.dirty = dirty
        self.metadata = metadata
        self._raw = self.metadata["ac_ast"]

    def save(self, msg): # pragma: no cover
        pass

    def find_ancestors(self, name):  # pylint: disable=unused-variable
        """Find ancestor BlockNodes with a given name"""
        return [ApacheBlockNode(name=assertions.PASS,
                                parameters=assertions.PASS,
                                ancestor=self,
                                filepath=assertions.PASS,
                                metadata=self.metadata)]


class ApacheCommentNode(ApacheParserNode):
    """ apacheconfig implementation of CommentNode interface """

    def __init__(self, **kwargs):
        comment, kwargs = util.commentnode_kwargs(kwargs)  # pylint: disable=unused-variable
        super(ApacheCommentNode, self).__init__(**kwargs)
        self.comment = comment

    def __eq__(self, other):  # pragma: no cover
        if isinstance(other, self.__class__):
            return (self.comment == other.comment and
                    self.dirty == other.dirty and
                    self.ancestor == other.ancestor and
                    self.metadata == other.metadata and
                    self.filepath == other.filepath)
        return False


class ApacheDirectiveNode(ApacheParserNode):
    """ apacheconfig implementation of DirectiveNode interface """

    def __init__(self, **kwargs):
        name, parameters, enabled, kwargs = util.directivenode_kwargs(kwargs)
        super(ApacheDirectiveNode, self).__init__(**kwargs)
        self.name = name
        self.parameters = parameters
        self.enabled = enabled
        self.include = None

    def __eq__(self, other):  # pragma: no cover
        if isinstance(other, self.__class__):
            return (self.name == other.name and
                    self.filepath == other.filepath and
                    self.parameters == other.parameters and
                    self.enabled == other.enabled and
                    self.dirty == other.dirty and
                    self.ancestor == other.ancestor and
                    self.metadata == other.metadata)
        return False

    def set_parameters(self, parameters):
        """Sets the parameters for DirectiveNode"""
        pass


class ApacheBlockNode(ApacheDirectiveNode):
    """ apacheconfig implementation of BlockNode interface """

    def __init__(self, **kwargs):
        super(ApacheBlockNode, self).__init__(**kwargs)
        self.children = ()

    def __eq__(self, other):  # pragma: no cover
        if isinstance(other, self.__class__):
            return (self.name == other.name and
                    self.filepath == other.filepath and
                    self.parameters == other.parameters and
                    self.children == other.children and
                    self.enabled == other.enabled and
                    self.dirty == other.dirty and
                    self.ancestor == other.ancestor and
                    self.metadata == other.metadata)
        return False

    def add_child_block(self, name, parameters=None, position=None):  # pylint: disable=unused-argument
        """Adds a new BlockNode to the sequence of children"""
        new_block = ApacheBlockNode(name=assertions.PASS,
                                    parameters=assertions.PASS,
                                    ancestor=self,
                                    filepath=assertions.PASS,
                                    metadata=self.metadata)
        self.children += (new_block,)
        return new_block

    def add_child_directive(self, name, parameters=None, position=None):  # pylint: disable=unused-argument
        """Adds a new DirectiveNode to the sequence of children"""
        new_dir = ApacheDirectiveNode(name=assertions.PASS,
                                      parameters=assertions.PASS,
                                      ancestor=self,
                                      filepath=assertions.PASS,
                                      metadata=self.metadata)
        self.children += (new_dir,)
        return new_dir

    # pylint: disable=unused-argument
    def add_child_comment(self, comment="", position=None):  # pragma: no cover

        """Adds a new CommentNode to the sequence of children"""
        new_comment = ApacheCommentNode(comment=assertions.PASS,
                                        ancestor=self,
                                        filepath=assertions.PASS,
                                        metadata=self.metadata)
        self.children += (new_comment,)
        return new_comment

    def find_blocks(self, name, exclude=True): # pylint: disable=unused-argument
        """Recursive search of BlockNodes from the sequence of children"""
        return [ApacheBlockNode(name=assertions.PASS,
                                parameters=assertions.PASS,
                                ancestor=self,
                                filepath=assertions.PASS,
                                metadata=self.metadata)]

    def find_directives(self, name, exclude=True): # pylint: disable=unused-argument
        """Recursive search of DirectiveNodes from the sequence of children"""
        return [ApacheDirectiveNode(name=assertions.PASS,
                                    parameters=assertions.PASS,
                                    ancestor=self,
                                    filepath=assertions.PASS,
                                    metadata=self.metadata)]

    def find_comments(self, comment, exact=False): # pylint: disable=unused-argument
        """Recursive search of DirectiveNodes from the sequence of children"""
        return [ApacheCommentNode(comment=assertions.PASS,
                                  ancestor=self,
                                  filepath=assertions.PASS,
                                  metadata=self.metadata)]

    def delete_child(self, child):  # pragma: no cover
        """Deletes a ParserNode from the sequence of children"""
        pass

    def unsaved_files(self):  # pragma: no cover
        """Returns a list of unsaved filepaths"""
        return [assertions.PASS]


interfaces.CommentNode.register(ApacheCommentNode)
interfaces.DirectiveNode.register(ApacheDirectiveNode)
interfaces.BlockNode.register(ApacheBlockNode)
